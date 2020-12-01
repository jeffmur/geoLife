from math import log10
from PIL.Image import alpha_composite
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#import shapely
import matplotlib.pyplot as plt
import math
from PIL import Image

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

    #print(f"Records: {len(df)}")
    # print("Bounding Box within range: ")
    #print(f"Latidude \t Min: {minLat:.6f} \t Max: {maxLat:.6f} ")
    # print(f"Longitude \t Min: {minLon:.6f} \t Max: {maxLon:.6f} ")

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

    # print(f"Total Width {bound_w} miles")
    # print(f"Total Length {bound_l} miles")

    # Cell size in lon/lat
    lat_cell = (cell_size / lat_deg)
    lon_cell = (cell_size / lon_deg)

    # print(f"Cell_Size -- Lat:{lat_cell} \t in Miles: {cell_size}")
    # print(f"Cell_Size -- Lon:{lon_cell} \t in Miles: {cell_size}")

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
    '''Frequency Matrix \n
    For every data point (lon, lat) within cell_size increment by 1'''
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
        # Difference between origin (minLat, minLon) and record.
        # Calculate the lat/lon point within cell_step_size
        # Modulate to remain within pixel bounds 

        l = round((abs(minLat - record['Latitude']) / lat_cell % (g_length-1)))
        w = round((abs(minLon - record['Longitude']) / lon_cell % (g_width-1)))
        freq_heat.loc[l,w] += 1

    return freq_heat

def takeLog(freq_heat, df):
    shape = freq_heat.shape
    log_freq = pd.DataFrame(0, index=range(shape[0]),columns=range(shape[1]))
    '''For each row, normalize each data point \n
    By their maximum values between 0 and 1'''
    # Log(sum{Freq / Max Value of image per month})
    maxVal = freq_heat.max().max()
    # For each row in dataframe
    for label, record in freq_heat.iterrows():
        # For each data point in row
        j = 0
        for i in range(0, len(record)):
            data = record[i]
            # Log_x(0) is 0/X == 0
            l = 0
            # Log_x(X) == 1 (infinitity)
            if(data == maxVal):
                l = 1
            # Else calc log
            elif(data != 0):
                l = math.log(data, maxVal)

            log_freq.loc[label,j] = l
            j+=1

    return log_freq


def plotHeatMap(freqDF, title, cell_size):
    '''Show Heat Map \n
    FreqDF: DataFrame which plots number of records at given cell\n
    user: Name/UID \n
    cell_size: size of cell within grid'''
    ax = plt.axes()
    sns.heatmap(freqDF, center=0, ax=ax)
    plt.ylim(reversed(plt.ylim()))
    ax.set_title(f"{title} w/ {cell_size} sq miles")
    plt.show()

def saveHeatMap(freqDF, title, path):
    '''Save Heat Map To PNG \n
    FreqDF: DataFrame which plots number of records at given cell\n
    user: Name/UID \n
    cell_size: size of cell within grid'''

    plt.figure(figsize=freqDF.shape)
    sns.heatmap(freqDF, vmin=0, vmax=1, annot=True)
    plt.savefig(f'{path}/{title}.png')

# Ex. split_by_month_output/000/2008_10.csv
def parseUserDate(path):
    '''Returns: \n
    data['user']: User Dir
    data['date']: Date of heatmap'''
    p = str(path).split('/')

    # user  name
    # 000   2008_10.csv
    user = p[len(p)-2]
    name = p[len(p)-1]

    # 2008_10  csv
    date = str(name).split('.')

    # Dictonary for intuitive call
    data = {
        'name' : user,
        'date' : date[0]
    }
    return data


##################################################
##################################################
##################################################

def monthHeatMap(outputDir, file, cell_size, pixelX, pixelY):
    '''Global Function that allows easy interface to generate one month heatmap for given path \n
    File: Path to csv file \n
    cell_size: in miles \n
    pixelX: Pixel Width Demension \n
    pixelY: Pixel Length Demension'''
    df = csv.oneMonth(file)
    bounds, cells, grid = setMap(df, pixelX, pixelY, cell_size)
    freqDF = create2DFreq(df, bounds, grid, cells)
    log_df = takeLog(freqDF, df)
    # Show date as title
    d = parseUserDate(file)
    user = d['name']
    date = d['date']
    pathOut = f"{outputDir}/{user}"
    
    saveHeatMap(log_df, date, pathOut)
    

def allUserMonths(dir, cell_size, pixelX, pixelY):
    '''Generate heatmap for each month at given path for User \n
    File: Path to csv files \n
    cell_size: in miles \n
    pixelX: Pixel Width Demension \n
    pixelY: Pixel Length Demension'''
    all_files = csv.getUserDir(dir)
    for f in all_files:
        # per month
        monthHeatMap('user_heatmap_output',f, cell_size, pixelX, pixelY)
        
def userHeatMap(dir, cell_size, pixelX, pixelY):
    '''Plot all user data to single heat map \n
    dir: Name of containing folder (not full path)'''
    df = csv.wholeDirectoryToDF(dir)
    bounds, cells, grid = setMap(df, pixelX, pixelY, cell_size)
    freq = create2DFreq(df, bounds, grid, cells)
    userDir = parseUserDate(dir)['user']

    plotHeatMap(freq, userDir, cell_size)

def getFreqInMonth(file, cell_size, pixelX, pixelY):
    '''Return Log DataFrame for a single FILE \n
    returns dataframe'''
    df = csv.oneMonth(file)
    bounds, cells, grid = setMap(df, pixelX, pixelY, cell_size)
    freqDF = create2DFreq(df, bounds, grid, cells)
    log_df = takeLog(freqDF, df)
    
    return log_df

def prodImage(path, cell_size, pixelX, pixelY):
    '''Returns Image (pixelX, pixelY) \n
    Representation (in black/white) of log dataframe'''
    df = getFreqInMonth(path, cell_size, pixelX, pixelY)

    img = Image.new('RGB', (pixelX, pixelY), color = 'red')
    pixels = img.load()

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            freq = int(255*df.loc[i,j])
            pixels[i,j] = (freq, freq, freq)

    return img

def prodImageForUser(output_dir, parse_dir, cell_size, pixelX, pixelY):
    '''Generate pixelX by pixelY for each month at given path for User \n
    File: Path to csv files \n
    cell_size: in miles \n
    pixelX: Pixel Width Demension \n
    pixelY: Pixel Length Demension'''
    all_files = csv.getUserDir(parse_dir)
    # dir = split_/NNN/file
    for f in all_files:
        print(f)
        # per month directory
        img = prodImage(f, cell_size, pixelX, pixelY)
        data = parseUserDate(f)
        # Save to OUTPUT / USER DIRECTORY / DATE
        img.save(f"{output_dir}/{data['date']}.png")