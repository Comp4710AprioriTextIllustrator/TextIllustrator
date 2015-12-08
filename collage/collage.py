#!/usr/bin/env python

import glob
import math
import os
import sys
from optparse import OptionParser

from PIL import Image, ImageFont, ImageDraw

import settings

def debug(s):
    sys.stderr.write('%s\n' % s)



def makeCollage( listFiles = [], *args):


    # List of input files.
    infiles = listFiles
    debug('Found %s input files.' % len(infiles))
	
    print infiles
	
    # Create canvas.
    tile_count = len(infiles) + settings.TILE_OFFSET
    COLS = settings.COLS
    ROWS = tile_count // COLS + (1 if tile_count % COLS else 0)
    imgsize = (2 * settings.PADDING + settings.TILE_SIZE[0] * COLS +
               settings.GAP * (COLS - 1),
               2 * settings.PADDING + settings.TILE_SIZE[1] * ROWS +
               settings.GAP * (ROWS - 1))
    img = Image.new('RGB', imgsize, settings.BGCOLOR)
    debug('Creating a grid with %s columns and %s rows.' % (COLS, ROWS))

	
    imgno = 0
    for tile_file in infiles:
        debug('Processing %s...' % tile_file)

        # Tile position.
        pos = imgno + settings.TILE_OFFSET
        x = pos % COLS
        y = pos // COLS
        # Offsets.
        xoff = settings.PADDING + x * (settings.TILE_SIZE[0] + settings.GAP)
        yoff = settings.PADDING + y * (settings.TILE_SIZE[1] + settings.GAP)

        tile = Image.open(tile_file)

        # Resize image if necessary
        if settings.RESIZE and tile.size != settings.TILE_SIZE:
            w_from, h_from = tile.size
            if (w_from / float(h_from) >
                settings.TILE_SIZE[0] / float(settings.TILE_SIZE[1])):
                w_to = settings.TILE_SIZE[0]
                h_to = int(w_to / float(w_from) * h_from)
            else:
                h_to = settings.TILE_SIZE[1]
                w_to = int(h_to / float(h_from) * w_from)
            tile = tile.resize((w_to, h_to), Image.ANTIALIAS)

        # Place tile on canvas.
        img.paste(tile, (xoff, yoff))
		

        imgno += 1

    # Post-process image.
    settings.post_process(img)

    # Save output file.
    debug('Writing output file: %s' % settings.OUTPUT_FILE)
    img.save(settings.OUTPUT_FILE, quality=95)

