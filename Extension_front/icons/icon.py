from PIL import Image, ImageDraw, ImageFont

print("Creating icons...")

import os

os.makedirs('icons', exist_ok=True)

for size in [16, 48, 128]:
    img = Image.new('RGB', (size, size), color='#3533cd')
    draw = ImageDraw.Draw(img)

    if size >= 48:
        margin = size // 4
        draw.ellipse([margin, margin, size - margin - 4, size - margin - 4],
                     outline='white', width=max(2, size // 20))

        handle_start = int(size * 0.7)
        handle_end = int(size * 0.9)
        draw.line([handle_start, handle_start, handle_end, handle_end],
                  fill='white', width=max(2, size // 20))
    else:
        draw.ellipse([2, 2, 14, 14], outline='white', width=1)

    img.save(f'icons/icon{size}.png')
    print(f" Created icon{size}.png")

print(" All icons created successfully!")