#!/home/jeffmur/anaconda3/envs/geoLife/bin/python

import pandas as pd
import os
import glob
from PIL import Image
from pathlib import Path
import sys
# import folium
from src import preprocess as pre
import numpy as np
import io
from PIL import Image
import math as math
from src import heatmap as heat

"""
INPUT: USER ID
OUTPUT: Points of Interest HTML & JSON file?
PURPOSE: Identify most frequenly visited locations for each user
         Overlay the output to a single map
"""
## MODULAR
dataDir = "/home/jeffmur/data/geoLife/user_by_month/"
gpsHeader = ["Latitude", "Longitude", "Zero", "Altitude", "Num of Days", "Date", "Time"]
outDir = f"/home/jeffmur/data/geoLife/gps_maps_month"

boundingBox = pre.fetchGeoLocation("Beijing, China")
## ---
mapColors = [
    "red",
    "blue",
    "green",
    "purple",
    "orange",
    "darkred",
    "lightred",
    "beige",
    "darkblue",
    "darkgreen",
    "cadetblue",
    "darkpurple",
    "white",
    "pink",
    "lightblue",
    "lightgreen",
    "gray",
    "black",
    "lightgray",
]

args = sys.argv

if len(args) <= 1:
    print(f"Usage: py3 gen_user_map.py {dataDir}/USER_ID ")
    print("Usage: See header of py file")
    exit()

path = args[1].split("/")
user = path[len(path) - 1]

print(f"--- ON USER: {user} ---")


def tallyMapping(points):
    """"""
    tally = {}

    for key in points:
        # Check for duplicates
        count = points.count(key)
        if count > 1:
            # Add 1 to existing key, otherwise set to 1
            tally[key] = tally.setdefault(key, 0) + 1

    mostFreqLocation = max(tally, key=tally.get)

    # VERBOSE
    print(f"Size of Tally Dictionary: {len(tally)}")
    print(f"Unique Tally Values : {np.unique(list(tally.values()))}")
    print(f"Most Frequent Location: {mostFreqLocation}")
    return tally, mostFreqLocation


def mappingMonth(map, pathToFile, monthIndex):
    """"""
    # import csv
    df = pd.read_csv(pathToFile, names=gpsHeader)

    # Global Var: bounding box
    df = pre.dropOutlyingData(df, boundingBox)

    # Keep Lon/Lat coordinates
    df = df[["Latitude", "Longitude"]]
    points = [tuple(x) for x in df.to_numpy()]

    # Generate Tally Dictionary (maps Locations to Number of Occurances)
    tally, mostFreqLoc = tallyMapping(points)

    # New color for each month
    color = mapColors[monthIndex]
    print(f"COLOR for {heat.parse4Date(pathToFile)} : {color}")

    # iterate through all locations
    for key in tally.keys():
        # Add markers to each point of interest and color code each month
        folium.CircleMarker(key, radius=0.5, color=color).add_to(map)

    folium.Marker(mostFreqLoc).add_to(map)
    folium.PolyLine(tally.keys(), color=color, weight=1.0, opacity=1.0).add_to(map)


p = Path(outDir)
p2 = Path(outDir + "/" + user)

if not (os.path.isdir(p)):
    p.mkdir()

if not (os.path.isdir(p2)):
    p2.mkdir()

# Concat all user_month files
allDirs = glob.glob(dataDir + user + "/*")

# Load map centered on city center point (Beijing, China)
my_map = folium.Map(location=[39.9075, 116.39723], zoom_start=14)
# Seperate colors per month
colorIndex = 0

for monthPath in allDirs:
    # date = heat.parse4Date(monthPath)
    print(monthPath)
    mappingMonth(my_map, monthPath, colorIndex)
    colorIndex += 1

my_map.save(f"{outDir}/{user}.html")
