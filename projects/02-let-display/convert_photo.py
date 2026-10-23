"""Convert a photo into a 128x64 monochrome MicroPython bitmap.

Run ``py convert_photo.py`` for a file picker, or pass an image path.
The generated BITMAP assignment can be pasted into main.py.
"""

import argparse
from pathlib import Path

from PIL import Image, ImageOps

WIDTH = 128
HEIGHT = 64


def floyd_steinberg(image: Image.Image) -> Image.Image:
    """Return a 1-bit image using Floyd-Steinberg error diffusion."""
    pixels = [float(value) for value in image.convert("L").tobytes()]
    result = Image.new("1", image.size)
    out = result.load()
    width, height = image.size

    for y in range(height):
        for x in range(width):
            i = y * width + x
            old = pixels[i]
            new = 255.0 if old >= 128 else 0.0
            out[x, y] = 1 if new else 0
            error = old - new
            if x + 1 < width:
                pixels[i + 1] += error * 7 / 16
            if y + 1 < height:
                if x:
                    pixels[i + width - 1] += error * 3 / 16
                pixels[i + width] += error * 5 / 16
                if x + 1 < width:
                    pixels[i + width + 1] += error / 16
    return result


def pack_mono_vlsb(image: Image.Image) -> bytes:
    """Pack pixels in MicroPython framebuf.MONO_VLSB order (white is 1)."""
    pixels = image.convert("1")
    data = bytearray(WIDTH * HEIGHT // 8)
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if pixels.getpixel((x, y)):
                data[x + (y // 8) * WIDTH] |= 1 << (y & 7)
    return bytes(data)


def convert(source: Path, output: Path) -> None:
    try:
        with Image.open(source) as original:
            # EXIF-aware orientation and center crop preserve the display's aspect ratio.
            image = ImageOps.exif_transpose(original).convert("RGB")
            image = ImageOps.fit(image, (WIDTH, HEIGHT), method=Image.Resampling.LANCZOS)
    except (OSError, ValueError) as exc:
        raise ValueError(f"Could not read image '{source}': {exc}") from exc

    monochrome = floyd_steinberg(image.convert("L"))
    data = pack_mono_vlsb(monochrome)
    output.parent.mkdir(parents=True, exist_ok=True)
    values = ",\n    ".join(", ".join(str(byte) for byte in data[i:i + 16])
                        for i in range(0, len(data), 16))
    output.write_text(f"BITMAP = bytearray((\n    {values}\n))\n", encoding="utf-8")
    print(f"Wrote bitmap snippet: {output} ({len(data)} bytes)")
    print("Copy the BITMAP assignment into main.py, replacing its marked placeholder.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", nargs="?", type=Path, help="source JPG, PNG, BMP, or other Pillow image")
    parser.add_argument("--output", type=Path, default=Path("output/photo_bitmap.py"))
    args = parser.parse_args()

    source = args.image
    if source is None:
        try:
            import tkinter as tk
            from tkinter import filedialog

            root = tk.Tk()
            root.withdraw()
            selected = filedialog.askopenfilename(
                title="Choose a photo for the OLED",
                filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.webp"), ("All files", "*.*")],
            )
            root.destroy()
            if not selected:
                print("No photo selected.")
                return
            source = Path(selected)
        except ImportError as exc:
            parser.error(f"File picker is unavailable; pass an image path instead ({exc})")

    if not source.is_file():
        parser.error(f"Image file does not exist: {source}")
    try:
        convert(source, args.output)
    except ValueError as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
