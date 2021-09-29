from math import log10
from PIL.Image import alpha_composite
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import seaborn as sns

# import shapely
import matplotlib.pyplot as plt
import math
from PIL import Image
import os

# TODO: importCSV methods
# import importCSV as csv
import src.preprocess as pre


def setMap(boundingBox, cell_size):
    """
    Create HeatMap Outline

    df: DataFrame (GeoLife)

    cell_size: in miles
    """

    ## Calculate bounds
    sLat = float(boundingBox[0])
    nLat = float(boundingBox[1])
    wLon = float(boundingBox[2])
    eLon = float(boundingBox[3])

    # all four corners
    SE = [sLat, eLon]
    SW = [sLat, wLon]
    NE = [nLat, eLon]
    NW = [nLat, wLon]

    bounds = {"SE": SE, "SW": SW, "NE": NE, "NW": NW}

    ## Calculate Haversine Distance of bounds
    # SW -> NW
    # Width
    dWest = pre.haversine_distance(SW[0], SW[1], NW[0], NW[1])

    # NW -> NE
    # Length
    dNorth = pre.haversine_distance(NW[0], NW[1], NE[0], NE[1])

    # Round val to the nearest 1
    length = math.ceil(dNorth)
    width = math.ceil(dWest)

    # Image Dimensions
    l_pix = int(math.ceil(length / cell_size))
    w_pix = int(math.ceil(width / cell_size))

    # Step Size for Lat/Lon comparison
    # Max distance / num of pixels
    step_length = (nLat - sLat) / l_pix  #  Step Lenth
    step_width = (eLon - wLon) / w_pix  #  Step Width

    # Steps in degrees
    step = {"width": step_width, "length": step_length}

    # Calculated Width and Length of image
    pix = {"length": l_pix, "width": w_pix}

    return bounds, step, pix


def create2DFreq(df, bounds, step, pix):
    """
    Frequency Matrix
    For every data point (lon, lat) within cell_size increment by 1
    """

    nLat = bounds["NE"][0]
    eLon = bounds["NE"][1]

    columns = pix["width"]
    rows = pix["length"]

    # print(f"{nLat} {eLon}")

    print(f"{rows}, {columns}")

    step_w = step["width"]
    step_l = step["length"]

    freq_heat = pd.DataFrame(0, index=range(rows + 1), columns=range(columns + 1))
    lonLat = df[df.columns[0:2]].to_numpy()
    # print("Entering FM")

    maxVal = 0

    for location in lonLat:
        # Difference between max Point (NE)
        # And Location (lonLat)
        # Within Frequency Matrix bounds

        r = round((nLat - location[0]) / step_l)

        c = round((eLon - location[1]) / step_w)

        if (c <= columns) and (c >= 0) and (r <= rows) and (r >= 0):
            freq_heat.loc[r, c] += 1

            if maxVal < freq_heat.loc[r, c]:
                maxVal = freq_heat.loc[r, c]

    return maxVal, freq_heat


def takeLog(maxVal, freq_heat):
    shape = freq_heat.shape
    log_freq = pd.DataFrame(0, index=range(shape[0]), columns=range(shape[1]))
    if maxVal <= 1:
        return log_freq
    """For each row, normalize each data point \n
    By their maximum values between 0 and 1"""

    for row in freq_heat.itertuples():
        # Need row index for assignment
        for c in range(1, len(row)):
            # Capture data point @ [row, column]
            data = row[c]
            # print(data, end="")
            # Expecting 0.5 -> inf (nan)
            d = pre.log_base(maxVal, data)

            # # -inf or < 0
            # if(d < 0): l = d * -1
            # # inf or > 0
            # else: l = d
            # print(f"Data: {data} ... logit: {d}")

            # row[0] = Index ; c = columns
            # Offest Columns by the included index
            log_freq.loc[row[0], c - 1] = d

    # print("Calculated Logit")

    return log_freq


# def plotHeatMap(freqDF, title, cell_size):
#     """Show Heat Map \n
#     FreqDF: DataFrame which plots number of records at given cell\n
#     user: Name/UID \n
#     cell_size: size of cell within grid"""
#     ax = plt.axes()
#     sns.heatmap(freqDF, center=0, ax=ax)
#     plt.ylim(reversed(plt.ylim()))
#     ax.set_title(f"{title} w/ {cell_size} sq miles")
#     plt.show()


# def saveHeatMap(freqDF, title, path):
#     """Save Heat Map To PNG
#     FreqDF: DataFrame which plots number of records at given cell\n
#     user: Name/UID \n
#     cell_size: size of cell within grid"""

#     plt.figure(figsize=freqDF.shape)
#     sns.heatmap(freqDF, vmin=0, vmax=1, annot=True)
#     plt.savefig(f"{path}/{title}.png")


# Ex. split_by_month_output/000/2008_10.csv
def parse4Date(path):
    l = len(path)
    return path[l - 11 : l - 4]


def parse4User(path):
    uid = path.split("/")
    return uid[len(uid) - 1]
