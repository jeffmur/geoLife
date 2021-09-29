#!/home/jeffmur/anaconda3/envs/mobility/bin/python
import sys
sys.path.append(".")
import src.heatmap as hp
import src.preprocess as pre
import src.frequency as fre
import src.config as c

import os
import glob
from pathlib import Path

dataDir = c.DATA_INPUT_DIR

gpsHeader = c.DATA_HEADERS

args = sys.argv

if len(args) <= 1:
    print(f"Usage: py3 gen_user_freq.py {dataDir}/USER_ID ")
    print("Usage: See dispatch.py")
    exit()

outDir = c.DATA_OUTPUT_DIR + f"gps_{c.CELL_SIZE}_all/"
p = Path(outDir)

if not (os.path.isdir(p)):
    p.mkdir()

boundingBox = [
    "39.7350200",
    "40.1073889",
    "116.1644800",
    "116.6597843",
]  # pre.fetchGeoLocation('Beijing, China')

for user in args[1:]:
    val = hp.parse4User(user)
    print(f"On User: {val} ..... ", end="")

    # temp = dataDir+val+'/'
    # user_months = glob.glob(temp+'*')
    # print(f"parsing {len(user_months)} months")

    fre.imagePerUser(
        boundingBox=boundingBox,
        userDir=user,
        outDir=outDir,
        cell_size=c.SQ_CELL,
    )
