import pillow_heif; pillow_heif.register_heif_opener()
from PIL import Image, ImageChops, ImageEnhance
import os

def make_ela(in_path, out_path="out/ela.png", quality=95, scale=15):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img = Image.open(in_path).convert("RGB")
    tmp = os.path.join(os.path.dirname(out_path), "_tmp_ela.jpg")
    img.save(tmp, "JPEG", quality=quality)             # recompress
    resaved = Image.open(tmp)
    ela = ImageChops.difference(img, resaved)
    ela = ImageEnhance.Brightness(ela).enhance(scale)  # amplify
    ela.save(out_path)
    return out_path
