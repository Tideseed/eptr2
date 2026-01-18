# Documentation Assets

This directory contains assets for the MkDocs documentation.

## Required Files

- `logo.png` - Logo image for the documentation header (recommended: 48x48 or 64x64 pixels)
- `favicon.ico` - Browser favicon

## Generating Placeholder Logo

If you don't have a logo yet, you can create a simple placeholder:

```python
# Using Pillow
from PIL import Image, ImageDraw, ImageFont

img = Image.new('RGB', (64, 64), color='#4F46E5')
d = ImageDraw.Draw(img)
d.text((12, 16), "E2", fill='white')
img.save('logo.png')
```

Or simply use any 64x64 PNG image as a placeholder.
