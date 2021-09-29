#!/home/jeffmur/anaconda3/envs/mobility/bin/python
import sys, os 
sys.path.append(".")
import src.config as c
import src.frequency as fre 
import matplotlib.pyplot as plt
import cv2
import numpy as np
from pathlib import Path
import src.heatmap as hp

photoDir = f"gps_{c.CELL_SIZE}_all/"

inputDir = c.DATA_OUTPUT_DIR + photoDir

outputDir = c.DATA_OUTPUT_DIR

## Usage: python resize.py {PATH_TO_USER.png}
args = sys.argv

if len(args) <= 1:
    print(f"Usage: py3 resize.py {photoDir}/USER_ID ")
    print("Usage: See dispatch.py")
    exit()

outDir = c.DATA_OUTPUT_DIR + f"resized_{c.CELL_SIZE}_all/"
p = Path(outDir)

if not (os.path.isdir(p)):
    p.mkdir()

# methods = [cv2.INTER_NEAREST, cv2.INTER_LINEAR, cv2.INTER_AREA, cv2.INTER_CUBIC, cv2.INTER_LANCZOS4]

for userDir in args[1:]:
    usr = hp.parse4User(userDir)
    print(f"On User: {usr} ..... ", end="")
    if(Path(f"{inputDir}{usr}.png").is_file()):
        img_resized = fre.resize(f"{inputDir}{usr}.png", 23, 15, cv2.INTER_AREA)
        plt.imsave(f"{outDir}{usr}.png", img_resized)