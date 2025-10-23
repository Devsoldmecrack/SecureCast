from pathlib import Path
from PIL import Image
import io
from PySide6.QtGui import QImage, QPainter, QGuiApplication
from PySide6.QtCore import QRectF, QBuffer, QByteArray, QIODevice
from PySide6.QtSvg import QSvgRenderer

base = Path(r"c:\\Users\\mainm\\Desktop\\SecureCast")
svg_path = base / "assets" / "icon.svg"
ico_path = base / "assets" / "icon.ico"

if not svg_path.exists():
    raise FileNotFoundError(f"SVG not found: {svg_path}")

app = QGuiApplication([])
renderer = QSvgRenderer(str(svg_path))
if not renderer.isValid():
    raise RuntimeError("Failed to load SVG with QSvgRenderer")

sizes = [16, 24, 32, 48, 64, 128, 256]
png_images = []

for s in sizes:
    img = QImage(s, s, QImage.Format.Format_RGBA8888)
    img.fill(0)
    painter = QPainter(img)
    
    renderer.render(painter, QRectF(0, 0, s, s))
    painter.end()
    
    ba = QByteArray()
    buf = QBuffer(ba)
    buf.open(QIODevice.WriteOnly)
    img.save(buf, "PNG")
    buf.close()
    pil = Image.open(io.BytesIO(bytes(ba)))
    png_images.append(pil)


png_images[0].save(ico_path, format="ICO", sizes=[(s, s) for s in sizes])
print(f"ICO created at: {ico_path}")
