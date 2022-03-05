import json
from pprint import pprint

import cv2
import numpy as np

with open("data/meta_singles.json", "r") as f:
    meta_data = json.load(f)

shapes = {}
for card in meta_data["singles"]:
    img = cv2.imread(card["path"])
    h, w, _ = img.shape
    
    if f"{h}_{w}" != "267_171":
        img = cv2.resize(img, (171, 267))
        print("Writing {}".format(card["path"]))
        cv2.imwrite(card["path"], img)
    
    if f"{h}_{w}" not in shapes:
        shapes[f"{h}_{w}"] = 1
    else:
        shapes[f"{h}_{w}"] += 1

pprint(shapes)
