"""Conform Data to yolov3 Format

Assumption:
    - All Images Present in source_dir
    - A training.csv file with each row depicting the following
        - Image_Name,x1,x2,y1,y2
            - Here x1, y1 and x2, y2 are bottom left and top right coordinates
            of the bounding box in the image

Moves the trainig images as per training.csv fro source_dir to
train_dir and creates a txt file corresponding to each image with containing
`class x y w h`

Note that (x,y) and (w,h) are coordinates and dimensions of the bounding
box relative to width and height of the entire image.

"""


import csv
import os
from tqdm import tqdm
from PIL import Image

source_dir = "hc/images"
train_dir = "hc/train"

boxes = open("hc/training.csv")

print("Reading Labels...")
with open("../clustering/results/labelled-data.txt") as f:
    labels = f.readlines()
    for i in tqdm(range(len(labels)), ascii=True):
        labels[i] = labels[i].split(",")
        labels[i] = (labels[i][0], int(labels[i][-1]))
    labels = dict(labels)

with open("hc/training.csv") as f:
    reader = csv.reader(f)
    next(reader)
    for row in tqdm(reader, total=14000, ascii=True):
        image = row[0]
        x1, x2, y1, y2 = list(map(int, row[1:]))
        tf = os.path.join(train_dir, image)
        af = os.path.join(train_dir, os.path.splitext(image)[0] + ".txt")

        im = Image.open(tf)
        iw, ih = im.size

        x = (x1 + x2) / (2 * iw)
        y = (y1 + y2) / (2 * ih)
        width = (x2 - x1) / iw
        height = (y2 - y1) / ih

        with open(af, "w") as annot:
            annot.write("{} {} {} {} {}".format(labels[image], x, y, width, height))
