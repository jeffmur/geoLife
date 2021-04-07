#!/home/jeffmur/anaconda3/envs/geoLife/bin/python

import heatmap as hp
import preprocess as pre
import frequency as fre
import pandas as pd
import os
import glob
from PIL import Image
from pathlib import Path
import sys

dataDir = "/home/jeffmur/data/geoLife/split_by_month_output/"

gpsHeader = ["Latitude", "Longitude", "Zero", "Altitude", "Num of Days", "Date", "Time"]

meters_size = 300  # sq meters
CELL_SIZE = meters_size * 0.00062137  # sq miles

args = sys.argv

if len(args) <= 1:
    print(f"Usage: py3 gen_user_freq.py {dataDir}/USER_ID ")
    print("Usage: See dispatch.py")
    exit()

outDir = f"/home/jeffmur/dev/testgeo/data/gps_{CELL_SIZE}_month/"
p = Path(outDir)

print(f"Going to generate {len(args)-1} of them...")

if not (os.path.isdir(p)):
    p.mkdir()


# HTTP
boundingBox = pre.fetchGeoLocation("Beijing, China")

for user in args[1:]:
    uid = user.split("/")
    val = uid[len(uid) - 1]
    print(f"On User: {val} ..... ", end="")
    fre.imagePerMonth(
        boundingBox=boundingBox,
        userDir=user,
        outDir=Path(os.path.join(outDir, val)),
        cell_size=CELL_SIZE,
    )
