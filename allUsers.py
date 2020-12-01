# Personal lib
import heatmap as hp 
from pathlib import Path

# Static
cell_size = 0.1 # square miles
LengthPixel = 15
WidthPixel = 23

# All user directories in '000' format
all_paths = ["{0:03}".format(i) for i in range(163, 182)]

# Iterate through every user
for user_dir in all_paths:
    output_dir = Path(f'user_heatmap_output/{user_dir}')
    output_dir.mkdir()
    hp.allUserMonths(user_dir, cell_size, WidthPixel, LengthPixel)