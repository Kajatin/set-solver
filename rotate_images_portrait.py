import os

from PIL import Image

root_path = "data/singles"
for img_p in os.listdir(root_path):
    img_full_path = os.path.join(root_path, img_p)
    img = Image.open(img_full_path)
    if img.height < img.width:
        img = img.transpose(Image.ROTATE_90)
        img.save(img_full_path)
        print("Processed: {}".format(img_full_path))
