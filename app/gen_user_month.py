#!/home/jeffmur/anaconda3/envs/mobility/bin/python

import sys
sys.path.append(".")
import src.heatmap as hp
import src.preprocess as pre
import src.frequency as fre
import src.config as c

import pandas as pd
import os
import glob
from PIL import Image
from pathlib import Path

dataDir = c.DATA_INPUT_DIR

gpsHeader = c.DATA_HEADERS

args = sys.argv

if len(args) <= 1:
    print(f"Usage: py3 gen_user_freq.py {dataDir}/USER_ID ")
    print("Usage: See dispatch.py")
    exit()

outDir = c.DATA_OUTPUT_DIR + f"gps_{c.CELL_SIZE}_month/"
p = Path(outDir)

print(f"Going to generate {len(args)-1} of them...")

if not (os.path.isdir(p)):
    p.mkdir()


# HTTP
boundingBox = [
    "39.7350200",
    "40.1073889",
    "116.1644800",
    "116.6597843",
]# pre.fetchGeoLocation("Beijing, China")

for user in args[1:]:
    uid = user.split("/")
    val = uid[len(uid) - 1]
    print(f"On User: {val} ..... ", end="")
    fre.imagePerMonth(
        boundingBox=boundingBox,
        userDir=user,
        outDir=Path(os.path.join(outDir, val)),
        cell_size=c.SQ_CELL,
    )
