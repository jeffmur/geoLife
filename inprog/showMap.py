import contextily as ctx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gp

# Longitude East  - West
# Latitude  North - South

def fetchMap():
    loc = ctx.Place('tongzhou district', zoom_adjust=1)  # zoom_adjust modifies the auto-zoom
    # Print some metadata
    for attr in ["w", "s", "e", "n", "place", "zoom", "n_tiles"]:
        print("{}: {}".format(attr, getattr(loc, attr)))
    # Show the map
    im1 = loc.im
    fig, axs = plt.subplots(1, 1, figsize=(15, 15))
    #ctx.plot_map(loc, ax=axs[0])
    beijing_img, beijing_ext = ctx.bounds2img(loc.w-0.5, loc.s+0.2, loc.e-0.5, loc.n+0.2, zoom=11, ll=True)
    beijing_img, beijing_ext = ctx.warp_tiles(beijing_img, beijing_ext, "EPSG:4326")
    ctx.plot_map(beijing_img, beijing_ext, ax=axs, title="Tongzhou District, Beijing")

    plt.show()

    return beijing_img, beijing_ext