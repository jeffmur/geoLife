## Temporary Path Storage for simple plug-in-play development
import os
import dotenv

dotenv.load_dotenv()

# API_KEY = os.getenv("API_KEY")
# """
# For gmaps Google Maps API
# """

# TO_CLUSTER_TSV = os.getenv("TO_CLUSTER_TSV")
# """
# Output of CNN-AE clustering and embedding
# """

# Friendly view of meters (ex. 300, 500, etc.)
CELL_SIZE = os.getenv("CELL_SIZE")
# In sq miles
SQ_CELL = float(CELL_SIZE) * 0.00062137 # sq miles

DATA_INPUT_DIR = os.getenv("DATA_INPUT_DIR")
"""
Note: Used with os.walk which assumes it is a directory (hence no trailing backslash)
Important: This is the RAW dataset (not santized or preprocessed)
"""

DATA_OUTPUT_DIR = os.getenv("DATA_OUTPUT_DIR")

DATASET = os.getenv("DATASET")
"""
Name of the dataset we are processing. Could be "GeoLife", "MDC", etc.
"""

DATA_HEADERS = {
    "MDC": [
        "Index", 
        "UID", 
        "Date", 
        "Time", 
        "Latitude", 
        "Longitude"],
    "GeoLife": [
        "Latitude",
        "Longitude",
        "Zero",
        "Altitude",
        "Num of Days",
        "Date",
        "Time",
    ],
}.get(DATASET)
"""
Path to parsed dataset / (mdc || geoLife || privamov || etc.) /user_by_month/ included
"""

# GEO_CLUSTER = os.getenv("GEO_CLUSTER")
