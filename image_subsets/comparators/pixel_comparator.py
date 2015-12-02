#!/bin/python
# -*- coding: utf-8 -*-

import sys

from PIL import Image

class PixelComparator(object):
    def compare(self, first_image, second_image):
        return first_image == second_image
    
def usage():
    print "python pixel_comparison.py <image1_path> <image2_path>"
    
if __name__=="__main__":
    if len(sys.argv) == 3:
        try:
            a = Image.open(sys.argv[1])
            b = Image.open(sys.argv[2])
            print PixelComparator().compare(a, b)
        except Error as e:
            usage()
    else:
        usage()