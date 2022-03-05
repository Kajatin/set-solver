import os
import json
import shutil
from datetime import datetime

from config import *

idx = 0
meta = {
    "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
    "count": idx,
    "singles": list(),
}

root_path = "data/raw/archive"
for count in os.listdir(root_path):
    if os.path.isdir(os.path.join(root_path, count)):
        for color in os.listdir(os.path.join(root_path, count)):
            if os.path.isdir(os.path.join(root_path, count, color)):
                for shape in os.listdir(os.path.join(root_path, count, color)):
                    if os.path.isdir(os.path.join(root_path, count, color, shape)):
                        for texture in os.listdir(os.path.join(root_path, count, color, shape)):
                            for img in os.listdir(os.path.join(root_path, count, color, shape, texture)):
                                ext = os.path.splitext(img)
                                filename = f"{color}_{count}_{shape}_{texture}_{idx}{ext[1]}"
                                new_path = f"data/singles/{filename}"
                                shutil.copy(os.path.join(root_path, count, color, shape, texture, img), new_path)
                                idx += 1

                                meta["singles"].append({
                                    "path": new_path,
                                    "filename": filename,
                                    "idx": idx-1,
                                    "color": list(COLORS.keys())[list(COLORS.values()).index(color)],
                                    "count": list(COUNTS.keys())[list(COUNTS.values()).index(count)],
                                    "shape": list(SHAPES.keys())[list(SHAPES.values()).index(shape)],
                                    "texture": list(TEXTURES.keys())[list(TEXTURES.values()).index(texture)],
                                })

for root_path in ["data/raw/data/test-v2", "data/raw/data/train-v2/labelled"]:
    for card_folder in os.listdir(root_path):
        count, color, texture, shape = card_folder.split("-")
        count = {"1": "one", "2": "two", "3": "three"}[count]
        if color == "purple":
            color = "blue"
        texture = {"striped": "partial", "solid": "full", "empty": "empty"}[texture]
        shape = {"diamonds": "diamond", "diamond": "diamond", "ovals": "oval", "oval": "oval", "squiggles": "squiggle", "squiggle": "squiggle"}[shape]

        for img in os.listdir(os.path.join(root_path, card_folder)):
            ext = os.path.splitext(img)
            filename = f"{color}_{count}_{shape}_{texture}_{idx}{ext[1]}"
            new_path = f"data/singles/{filename}"
            shutil.copy(os.path.join(root_path, card_folder, img), new_path)
            idx += 1

            meta["singles"].append({
                "path": new_path,
                "filename": filename,
                "idx": idx-1,
                "color": list(COLORS.keys())[list(COLORS.values()).index(color)],
                "count": list(COUNTS.keys())[list(COUNTS.values()).index(count)],
                "shape": list(SHAPES.keys())[list(SHAPES.values()).index(shape)],
                "texture": list(TEXTURES.keys())[list(TEXTURES.values()).index(texture)],
            })

meta["count"] = idx

with open("data/meta_singles.json", "w") as f:
    json.dump(meta, f, indent=4)