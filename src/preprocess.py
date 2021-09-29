# Pre-Processes raw data to be set in dataframe
# Jeffrey Murray Jr

import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
import time
from pprint import pprint
import os
from datetime import date
from pathlib import Path
import math as m

## Raw Data Processing ##


def removeSpaces(toRemove, toSave):
    """
    Remove extra spaces in src file,
    Then saves to dst file.

    :param: toRemove: path to source file

    :param: toSave: path to destination file
    """
    fin = open(toRemove, "rt")
    fout = open(toSave, "wt")

    for line in fin:
        fout.write(" ".join(line.split()))
        fout.write("\n")

    fin.close()
    fout.close()


## Formatted Data Processing ##


def toPandas(pathToFile, nameSpace, delim):
    """
    Returns dataframe with labeled header

    :param: pathToFile : full UNIX Path

    :param: nameSpace : data labels (aka headers)

    :param: delimeter : Expected ' ' or ','
    """
    df = pd.read_table(pathToFile, sep=delim, names=nameSpace)
    df.head()
    return df


def fetchGeoLocation(cityCountry):
    """
    Using Nominatim OpenAPI to fetch Longitude and Latitude Data
    :return: [south Latitude
            north Latitude,
            west Longitude,
            east Longitude]

    :param: cityCountry : format string 'city, country code' ex. 'Lynon, France'
    """
    # HTTP Request recommended : "Application Name"
    app = Nominatim(user_agent="geoLife")
    location = app.geocode(cityCountry).raw
    # pprint(location) # pretty print JSON returned from OpenStreetMap dataset

    return location["boundingbox"]


def dropOutlyingData(df, boundingbox):
    """
    Remove data outside of bounding box longitude and latitude.

    :param: Dataframe with ['Longitude'] and ['Latitude'] column labels

    :param: Bounding Box : [min Lat, max Lat, min Lon, max Lon]
    """
    lat = boundingbox[0:2]
    lon = boundingbox[2:4]

    # Query data within bounds as forced floats
    return df.loc[
        (df.Longitude >= float(lon[0]))
        & (df.Longitude <= float(lon[1]))
        & (df.Latitude >= float(lat[0]))
        & (df.Latitude <= float(lat[1]))
    ].reset_index(drop=True)


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculates the Distance between two coordinates (Lon/Lat)

    :input: lat1, lon1, lat2, lon2

    :returns: (in miles) distance between points
    """
    r = 6371
    phi1 = m.radians(lat1)
    phi2 = m.radians(lat2)
    delta_phi = m.radians(lat2 - lat1)
    delta_lambda = m.radians(lon2 - lon1)
    a = (
        np.sin(delta_phi / 2) ** 2
        + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda / 2) ** 2
    )
    res = r * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)))
    return np.round(res, 2) * 0.62137  # 1km to miles


# Input: 0 -> 1
# Output: -inf + +inf
def logit(p):
    epsilon = 0.0000001
    return m.log(p + epsilon / (1 + epsilon - p))


# def inv_logit(p):
#     return np.exp(p) / (1 + np.exp(p))


def log_base(max, val):
    if val == 0:
        return 0

    return m.log(val, max)


def logit_base(max, val):
    inn = log_base(max, val)

    return logit(inn)
