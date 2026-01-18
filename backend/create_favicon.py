from PIL import Image, ImageDraw
import os

# Create a simple 16x16 black square with a white border
img = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)
draw.rectangle([1, 1, 14, 14], fill='white')
draw.rectangle([0, 0, 15, 15], outline='white')

# Save as ICO file
favicon_path = os.path.join('app', 'static', 'favicon.ico')
os.makedirs(os.path.dirname(favicon_path), exist_ok=True)
img.save(favicon_path, format='ICO', sizes=[(16, 16)])
