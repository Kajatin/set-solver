import random
import json
from datetime import datetime

import cv2
import numpy as np
from tqdm import tqdm

from config import *

with open("data/meta_singles.json", "r") as f:
    meta_data = json.load(f)
singles = meta_data["singles"]
num_singles = meta_data["count"]

annotation = {
    "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
    "count": 0,
    "mats": list(),
}

for idx in tqdm(range(1)):
# for idx in tqdm(range(num_singles//12)):
    selection = random.choices(singles, k=12)
    # print(selection)

    codes = {}
    canvas = np.zeros((981, 1004, 3), dtype=np.uint8)
    r = 0
    c = 0
    r_slack = 30
    c_slack = 40
    for card in selection:
        img = cv2.imread(card["path"])
        h, w, _ = img.shape
        center = [r*h + h/2 + (r*2+1)*r_slack, c*w + w/2 + (c*2+1)*c_slack]
        center[0] += random.randint(-r_slack, r_slack)
        center[1] += random.randint(-c_slack, c_slack)
        canvas[int(center[0] - h/2):int(center[0] + h/2), int(center[1] - w/2):int(center[1] + w/2), :] = img
        
        code = f"{r}_{c}"
        color, count, shape, texture, *_ = card["filename"].split("_")
        codes[code] = {
            "color": list(COLORS.keys())[list(COLORS.values()).index(color)],
            "count": list(COUNTS.keys())[list(COUNTS.values()).index(count)],
            "shape": list(SHAPES.keys())[list(SHAPES.values()).index(shape)],
            "texture": list(TEXTURES.keys())[list(TEXTURES.values()).index(texture)],
            "center": [center[0] / canvas.shape[0], center[1] / canvas.shape[1]],
        }
        
        if c < 3:
            c += 1
        else:
            c = 0
            r += 1

    filename = f"mat_{idx}.png"
    file_path = f"data/mats/{filename}"
    annotation["mats"].append({
        "path": file_path,
        "filename": filename,
        "idx": idx,
        "cards": codes,
    })
    cv2.imwrite(file_path, canvas)
    cv2.imshow("canvas", canvas)
    cv2.waitKey(0)

annotation["count"] = idx + 1

with open("data/mats_annotation.json", "w") as f:
    json.dump(annotation, f, indent=4)
