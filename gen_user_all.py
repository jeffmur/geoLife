#!/home/jeffmur/anaconda3/envs/geoLife/bin/python

import heatmap as hp 
import preprocess as pre 
import frequency as fre

import os
import glob
from pathlib import Path
import sys

dataDir = '/home/jeffmur/data/geoLife/split_by_month_output/'

gpsHeader = ['Latitude', 'Longitude', 'Zero', 'Altitude', 'Num of Days', 'Date', 'Time']

meters_size = 300 # sq meters
CELL_SIZE = meters_size * 0.00062137 #sq miles

args = sys.argv

if(len(args) <= 1):
    print(f"Usage: py3 gen_user_freq.py {dataDir}/USER_ID ")
    print("Usage: See dispatch.py")
    exit()

outDir = f'/home/jeffmur/dev/testgeo/data/gps_{CELL_SIZE}_all/'
p = Path(outDir)

if(not (os.path.isdir(p))):
    p.mkdir()

boundingBox = pre.fetchGeoLocation('Beijing, China')

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
        cell_size=CELL_SIZE,
    )