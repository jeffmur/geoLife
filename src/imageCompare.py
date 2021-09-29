# from frequency import genFMprime
import pandas as pd
import numpy as np
import cv2

from PIL import Image
# import seaborn as sns
import matplotlib.pyplot as plt
import pylab as plot
import skimage.metrics as ski

import os
from pathlib import Path
import src.preprocess as pre


def ssimImage(df):
    """"""
    dim = df.shape

    img = Image.new("RGB", (dim[0], dim[1]), color="red")
    pixels = img.load()

    for row in df.itertuples():
        # Need row index for assignment
        for c in range(1, len(row)):
            # Capture data point @ [row, column]
            data = row[c]

            freq = int(255 * data)

            pixels[row[0], c - 1] = (0, freq, 0)

    return img


# 2. Construct the argument parse and parse the arguments
def ssim(fn, fns):
    """"""
    # 3. Load the two input images
    imageA = cv2.imread(fn)

    all_scores = []


    for f in fns:
        imageB = cv2.imread(f)
        score = ski.structural_similarity(imageA, imageB, gaussian_weights=True, multichannel=True)
        all_scores.append(score)

    
    #print("{:24} {:.4f}".format(os.path.basename(fn), np.mean(all_scores)))

    return all_scores


def createSSIMimage(data_directory):
    """"""
    parseDir = Path(data_directory).rglob("*.png")

    all = sorted(parseDir, key=lambda i: os.path.splitext(os.path.basename(i))[0])
    files = [str(x) for x in all]

    df = pd.DataFrame(index=range(len(files)),columns=range(len(files)))
    to_append = []
    i = 0
    for A in files:
        to_append = ssim(A, files[:])
        
        df.loc[i] = to_append
        i+=1

    # Generate Image
    return df, ssimImage(df)


##
##
##
def mse(first, second):
    """"""
    # Load the two input images
    imageA = cv2.imread(first)
    imageB = cv2.imread(second)
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    # return mean_squared_error(imageA, imageB)
    return ski.mean_squared_error(imageA, imageB)


def mseImage(df):
    """"""
    dim = df.shape

    img = Image.new("RGB", (dim[0], dim[1]), color="red")
    pixels = img.load()

    for row in df.itertuples():
        # Need row index for assignment
        for c in range(1, len(row)):
            # Capture data point @ [row, column]
            data = row[c]

            freq = int(255 * data)

            pixels[row[0], c - 1] = (0, 255 - freq, 0)

    return img


def createMSEimage(data_directory):
    """"""
    parseDir = Path(data_directory).rglob("*.png")

    all = sorted(parseDir, key=lambda i: os.path.splitext(os.path.basename(i))[0])
    files = [x for x in all]

    df = pd.DataFrame(index=range(len(files)),columns=range(len(files)))
    to_append = []
    i = 0
    for A in files:
        fileA = (str(A).split("'"))[0]
        for B in files:
            fileB = (str(B).split("'"))[0]
            to_append.append(mse(fileA, fileB))

        df.loc[i] = to_append
        to_append = []
        i += 1

    # Generate Image
    return mseImage(takeLog(df))


def takeLog(df):
    """"""
    maxVal = df.max().max()
    shape = df.shape
    log_freq = pd.DataFrame(0, index=range(shape[0]), columns=range(shape[1]))
    if maxVal <= 1:
        return log_freq

    for row in df.itertuples():
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

def L2Norm(H1,H2):
    distance =0
    for i in range(len(H1)):
        distance += np.square(H1[i]-H2[i])
    return np.sqrt(distance)