import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gp
import seaborn as sns
import shapely
import matplotlib.pyplot as plt

# Personal lib
import importCSV as csv

def setMap(df, gX, gY, cell_size):
    '''Create HeatMap Outline \n
        df: DataFrame (GeoLife) \n
        gX: Length in pixels (15) \n
        gY: Width in pixels (23) \n
        cell_size: in miles'''

    # Calculate bounds
    maxLat = max(df['Latitude'])
    minLat = min(df['Latitude'])
    maxLon = max(df['Longitude'])
    minLon = min(df['Longitude'])

    bounds = {
        'minLat' : minLat,
        'maxLat' : maxLat,
        'minLon' : minLon,
        'maxLon' : maxLon
    }

    print(f"Number of records for user: {len(df)}")
    print("Bounding Box within range: ")
    print(f"Latidude \t Min: {minLat} \t Max: {maxLat} ")
    print(f"Longitude \t Min: {minLon} \t Max: {maxLon} ")

    # Longitude East  - West
    # Latitude  North - South
    # total area for the grid
    north = maxLat # y max
    south = minLat # y min
    east = minLon # x max
    west = maxLon # x min

    # Create bounding box
    width = west - east     # Latitude
    length = north - south   # Longitude

    # Assumption Length x Width for 2D image rep
    grid_size = (gX, gY)

    # going off that assumption
    g_length = grid_size[0]
    g_width = grid_size[1]
    t_pixels = g_length * g_width

    # Rough estimate conversion table
    lat_deg = 69 #mi for Lat
    lon_deg = 60 #mi for Lon

    # Convert width & length to miles
    bound_w = width * lat_deg   # m in miles
    bound_l = length * lon_deg  # n in miles

    print(f"Total Width {bound_w} miles")
    print(f"Total Length {bound_l} miles")

    # Cell size in lon/lat
    lat_cell = (cell_size / bound_w) / lat_deg
    lon_cell = (cell_size / bound_l) / lon_deg

    cells = {
        'lat' : lat_cell,
        'lon' : lon_cell
    }

    grid = {
        'l' : g_length,
        'w' : g_width
    }

    return bounds, cells, grid 

def create2DFreq(df, bounds, grid, cells):
    minLat = bounds['minLat']
    minLon = bounds['minLon']

    lon_cell = cells['lon']
    lat_cell = cells['lat']

    g_length = grid['l']
    g_width = grid['w']

    rows = grid['l']
    columns = grid['w']
    freq_heat = pd.DataFrame(0, index=range(rows),columns=range(columns))
    for label, record in df.iterrows():
        l = round((abs(minLat - record['Latitude']) / lat_cell) % (g_length-1))
        w = round((abs(minLon - record['Longitude']) / lon_cell) % (g_width-1))
        freq_heat.loc[l,w] += 1

    return freq_heat

def plotHeatMap(freqDF, date, cell_size):
    '''Show Heat Map \n
    FreqDF: DataFrame which plots number of records at given cell\n
    user: Name/UID \n
    cell_size: size of cell within grid'''

    ax = plt.axes()
    sns.heatmap(freqDF, center=0, ax=ax)
    ax.set_title(f"{date} w/ {cell_size} sq miles")
    plt.show()

##################################################
##################################################
##################################################

def monthHeatMap(file, cell_size, gridX, gridY):
    '''Global Function that allows easy interface to generate one month heatmap for given path \n
    File: Path to csv file \n
    cell_size: in miles \n
    gridX: Pixel Width Demension \n
    gridY: Pixel Length Demension'''
    df = csv.oneMonth(file)
    bounds, cells, grid = setMap(df, gridX, gridY, cell_size)
    freqDF = create2DFreq(df, bounds, grid, cells)

    # Get the Date from path
    path = str(file).split('/')
    name = path[len(path)-1]
    date = str(name).split('.')
    plotHeatMap(freqDF, date[0], cell_size)