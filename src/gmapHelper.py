import gmaps
import pandas as pd
import preprocess as pre
import numpy as np
import config as c

import skmob.utils.plot as p
import folium

from skmob.utils.plot import HeatMap

from skmob.preprocessing import filtering, detection, clustering
from skmob.preprocessing import compression
import skmob

parsedPath = c.DATA_INPUT_DIR
boundingBox = pre.fetchGeoLocation("Haidian District")
gpsHeaders = c.DATA_HEADERS

# Luassane (MDC)
# ["46.5043006", "46.6025773", "6.5838681", "6.7208137"]

# Beijing, China
# 39.7350200, 40.1073889, 116.1644800, 116.6597843
# Ex. /data/jeffmur/mdcdOut/gps_0.186411_month/5448/2009_10.png


def parse4Date(path):
    l = len(path)
    return path[l - 11 : l - 4]


def parse4User(path):
    uid = path.split("/")
    return uid[len(uid) - 2]


############ DECODING UID CLUSTERS & MAPS ############

def plotCompressCluster(clusterID, dictOfClusters, uidMapping, map, color):
    df = compressWeighHeatMap(clusterID, dictOfClusters, uidMapping)
    df = df.drop(['Zero', 'Altitude', 'Num of Days', 'Date', 'Time'], axis=1)
    p.HeatMap(df.iloc[:, [0,1]], gradient=[color], radius=10, blur=10).add_to(map)


def compressWeighHeatMap(clusterID, clustersOfUID, uidMap):
    """
    Input: dataframe[(Latitude, Longitude), ... , N]

    """
    # Great list of all (old) paths to months in cluster
    months = (np.array(clustersOfUID[clusterID]).tolist())[0]

    # Get data corresponding to a single month ID
    listOfUID = mapKeys(uidMap, months)

    print(f"Number of months in cluster: {len(listOfUID)}")

    # Dataframe of all user data in cluster
    oneCluster = monthCluster(listOfUID)

    tdf = skmob.TrajDataFrame(oneCluster)
    # compress the trajectory using a spatial radius of 0.2 km
    ctdf = compression.compress(tdf, spatial_radius_km=0.2)
    # print the difference in points between original and filtered TrajDataFrame
    print('Points of the original trajectory:\t%s'%len(tdf))
    print('Points of the compressed trajectory:\t%s'%len(ctdf))
    return ctdf


def getLatLon(clusterID):
    df = pd.read_csv(f"{c.GEO_CLUSTER}{clusterID}_cluster.csv")

    # TMP
    # df = df.head(500)

    return (df.iloc[:, [1, 2]])


def heatmap_layer(clusterID, color):
    return gmaps.heatmap_layer(
        getLatLon(clusterID), gradient=['white', 'blue', 'red']
    )


def saveClusterToCSV(clusterID, uidMap, dict):
    # Gather all data in cluster via heatmap
    clusterLoc = getHeatMapLayer(clusterID, uidMap, dict, None).locations

    # create df
    df = pd.DataFrame(clusterLoc, columns=["Latitude", "Longitude"])

    # saveToFile
    df.to_csv(c.GEO_CLUSTER + f"{clusterID}_cluster.csv")


def mapKeys(rawUIDPath, targetKeys):
    """
    Returns lists of paths from UID key
    """
    npMonths = rawUIDPath.to_numpy()

    listOfUID = []

    for key in targetKeys:
        listOfUID.append(npMonths[key][1])

    return listOfUID


def monthCluster(UIDPath):  # color
    """
    Input: List of UIDPaths
    Ex: [0, '/data/jeffmur/mdcdOut/gps_0.186411_month/5448/2009_10.png']

    Purpose: Plot uid's real-world location in Google Maps

    Result: Returns Layer of cluster group
    """
    frames = []

    ## Concats all images to the same dataframe

    for oneMonth in UIDPath:
        # Get username & date from image path
        date = parse4Date(oneMonth)
        user = parse4User(oneMonth)

        # Import location data from a single image
        onefile = pd.read_csv(f"{parsedPath}/{user}/{date}.csv", names=gpsHeaders)

        boundedFile = pre.dropOutlyingData(onefile, boundingBox)

        newName = { 'Latitude': 'lat', 'Longitude': 'lng'}
  
        # call rename () method
        boundedFile.rename(columns=newName,
                inplace=True)

        boundedFile['datetime']=pd.to_datetime(boundedFile.Date+ ' '+boundedFile.Time, format='%Y/%m/%d %H:%M:%S')

        # Finally, append to frames lookup
        frames.append(boundedFile)

    ## Now all frames have been placed into dataframe
    df = pd.concat(frames, sort=False)

    return df #, gmaps.heatmap_layer(df, opacity=0.75, point_radius=3, gradient=color)


def mostFreqTally(points):
    tally = {}

    for key in points:
        # Check for duplicates
        count = points.count(key)
        if count > 1:
            # Add 1 to existing key, otherwise set to 1
            tally[key] = tally.setdefault(key, 0) + 1

    print(len(tally))
    uniqueTuples = np.unique(points, axis=0)
    print(len(uniqueTuples))

    mostFreqLocation = max(tally, key=tally.get)

    print(mostFreqLocation)
    return tally


def mapClustersToUID(indexToCluster):
    """
    Input: Array of Cluster ID where the index value corresponds to the output of image_list.txt indices

    Out: Dictonary where cluster 0 = months UID [a, b, c, d, ... , z]
    """
    clustersOfUID = {}

    # N num of clusters
    for i in range(0, max(indexToCluster) + 1):
        # Get list of images in cluster i
        listOfImages = np.where(indexToCluster == i)
        # Add list to dictonary
        clustersOfUID[i] = listOfImages

    return clustersOfUID


def plotCluster(clusterID, uidMap, clustersOfUID):

    # Concat all months into a list
    months = (np.array(clustersOfUID[clusterID]).tolist())[0]

    # Get data corresponding to a single month ID
    listOfUID = mapKeys(uidMap, months)

    print(f"Number of months in cluster: {len(listOfUID)}")

    # Heatmap layer
    oneCluster = monthCluster(listOfUID, None)

    # Plot on Google Maps via gmaps
    # TODO: set API token as .env var
    gmaps.configure(api_key=c.API_KEY)  # Your Google API key
    fig = gmaps.figure()
    fig.add_layer(oneCluster)
    return fig


def getHeatMapLayer(clusterID, uidMap, clustersOfUID, color):

    # Concat all months into a list
    months = (np.array(clustersOfUID[clusterID]).tolist())[0]

    # Get data corresponding to a single month ID
    listOfUID = mapKeys(uidMap, months)

    print(f"Number of months in cluster: {len(listOfUID)}")

    # Heatmap layer
    oneCluster = monthCluster(listOfUID, color)

    return oneCluster


def plotClusterLayer(oneCluster):
    # Plot on Google Maps via gmaps
    # TODO: set API token as .env var
    gmaps.configure(api_key=c.API_KEY)  # Your Google API key
    fig = gmaps.figure(
        display_toolbar=False,
        layout={
            "width": "400px",
            "height": "600px",
            "padding": "3px",
            "border": "1px solid black",
        },
    )
    fig.add_layer(oneCluster)
    return fig
