import gmaps
import pandas as pd
import preprocess as pre
import numpy as np

parsedPath = '/home/jeffmur/data/mdcd/user_by_month'
boundingBox = ['46.5043006', '46.6025773', '6.5838681', '6.7208137'] 

# Ex. /data/jeffmur/mdcdOut/gps_0.186411_month/5448/2009_10.png
def parse4Date(path):
    l = len(path)
    return path[l-11:l-4]

def parse4User(path):
    uid = path.split('/')
    return uid[len(uid)-2]

def mapKeys(rawUIDPath, targetKeys):
    """
    Returns lists of paths from UID key
    """
    npMonths = rawUIDPath.to_numpy()

    listOfUID = []

    for key in targetKeys:
        listOfUID.append(npMonths[key][1])

    return listOfUID

def monthCluster(UIDPath, color): #color 
    """
    Input: List of UIDPaths
    Ex: [0, '/data/jeffmur/mdcdOut/gps_0.186411_month/5448/2009_10.png']

    Purpose: Plot uid's real-world location in Google Maps

    Result: Returns Layer of cluster group
    """ 
    frames = []

    for oneMonth in UIDPath:
        # Get username & date from image path       
        date = parse4Date(oneMonth)
        user = parse4User(oneMonth)

        # Import location data from a single image
        onefile = pd.read_csv(f'{parsedPath}/{user}/{date}.csv')

        boundedFile = pre.dropOutlyingData(onefile, boundingBox)
        
        # Create dataframe of month
        month_df = boundedFile[['Latitude', 'Longitude']]
        frames.append(month_df)

    df = pd.concat(frames, sort=False)

    points = [tuple(x) for x in df.to_numpy()]
    # cluster_layer = gmaps.symbol_layer(
    #     df, fill_color=color, stroke_color=color, scale=2
    # )

    return points, gmaps.heatmap_layer(df, opacity=1, gradient=color)


def mostFreqTally(points):
    tally = {}

    for key in points:
        # Check for duplicates
        count = points.count(key)
        if(count > 1):
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
    for i in range(0,max(indexToCluster)+1):
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

    print(f'Number of months in cluster: {len(listOfUID)}')

    # Heatmap layer
    points, oneCluster = monthCluster(listOfUID, None)

    # Plot on Google Maps via gmaps
    # TODO: set API token as .env var
    gmaps.configure(api_key="AIzaSyDwyxavuW2jOi2zifvXSzdOOyVr7UKL8Iw") # Your Google API key
    fig = gmaps.figure()
    fig.add_layer(oneCluster)
    return fig


def getClusterLayer(clusterID, uidMap, clustersOfUID, color):

    # Concat all months into a list
    months = (np.array(clustersOfUID[clusterID]).tolist())[0]
    
    # Get data corresponding to a single month ID
    listOfUID = mapKeys(uidMap, months)

    print(f'Number of months in cluster: {len(listOfUID)}')

    # Heatmap layer
    points, oneCluster = monthCluster(listOfUID, color)

    return oneCluster

def plotClusterLayer(oneCluster):
    # Plot on Google Maps via gmaps
    # TODO: set API token as .env var
    gmaps.configure(api_key="AIzaSyDwyxavuW2jOi2zifvXSzdOOyVr7UKL8Iw") # Your Google API key
    fig = gmaps.figure()
    fig.add_layer(oneCluster)
    return fig