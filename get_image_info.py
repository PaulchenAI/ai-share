import os
from PIL import Image

def get_image_info(directory):
    files = sorted(os.listdir(directory))
    for f in files:
        if f.endswith('.png'):
            path = os.path.join(directory, f)
            with Image.open(path) as img:
                print(f"{f}: {img.width}x{img.height} (ratio: {img.width/img.height:.2f})")

if __name__ == '__main__':
    get_image_info('sucai')
