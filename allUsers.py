# Personal lib
import heatmap as hp 
from pathlib import Path
import PIL
import os
# Static
cell_size = 0.1 # square miles
LengthPixel = 15
WidthPixel = 23

dataIn = 'split_by_month_output/'
targetOut = 'user_pil_output/'

# All user directories in '000' format
all_paths = ["{0:03}".format(i) for i in range(0, 182)]

# Iterate through every user
for user_dir in all_paths:
    target = Path(targetOut)
    output_dir = Path(f'{targetOut}/{user_dir}')
    print(user_dir)
    if(not os.path.isdir(targetOut)):
        target.mkdir()
    if(not os.path.isdir(output_dir)):
        output_dir.mkdir()

    hp.prodImageForUser(output_dir, user_dir, cell_size, WidthPixel, LengthPixel)