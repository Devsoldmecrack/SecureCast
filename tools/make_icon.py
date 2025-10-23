from pathlib import Path
import io
from PIL import Image
import cairosvg

base = Path(r"c:\Users\mainm\Desktop\SecureCast")
svg = base / "assets" / "icon.svg"
ico = base / "assets" / "icon.ico"

if not svg.exists():
    raise FileNotFoundError(f"SVG not found: {svg}")

sizes = [16, 24, 32, 48, 64, 128, 256]

png_bytes = cairosvg.svg2png(url=str(svg), output_width=1024, output_height=1024)
img = Image.open(io.BytesIO(png_bytes)).convert("RGBA")
imgs = [img.resize((s, s), Image.LANCZOS) for s in sizes]

imgs[0].save(ico, format="ICO", sizes=[(s, s) for s in sizes])
print(f"ICO created at: {ico}")
