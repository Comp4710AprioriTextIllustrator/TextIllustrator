import os


# Size of every image tile.
#To decrease white space vertically lower the Y value of TILE_SIZE
TILE_SIZE = 160, 175
RESIZE = True  # Resize files that don't match the above?

# Column width of image grid. Rows will be determined automatically.
COLS = 6

# Tile offset.
# 0 will start at the top right, 1 will leave one empty tile, etc.
TILE_OFFSET = 0

# Outside padding (in px)
PADDING = 5

# Gap size between images (in px)
GAP = 2

# Background color
BGCOLOR = '#fff'

# Output dir
subdir = lambda *d: os.path.join(os.path.dirname(__file__), *d)


#change out put directory and file name of collage here
OUTPUT_FILE = subdir('output', 'fullcollage1.jpg')


# Post-processing of image. Default: Do nothing.
post_process = lambda img: None
