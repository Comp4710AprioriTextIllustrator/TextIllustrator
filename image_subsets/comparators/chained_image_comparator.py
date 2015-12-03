#!/bin/python
# -*- coding: utf-8 -*-

import pixel_comparator
import sys

from PIL import Image

class ChainedImageComparator(object):
    def __init__(self, image_comparators=[pixel_comparator.PixelComparator()], num_true_required=1):
        self.image_comparators = image_comparators
        self.num_true_required = num_true_required
        
    def compare(self, first_image, second_image):
        num_true = 0
        for comparator in self.image_comparators:
            if comparator.compare(first_image, second_image):
                num_true += 1
        
        return num_true >= self.num_true_required

def usage():
    print "python chained_image_comparison.py <image1_path> <image2_path>"
    
if __name__=="__main__":
    if len(sys.argv) == 3:
        try:
            a = Image.open(sys.argv[1])
            b = Image.open(sys.argv[2])
            print ChainedImageComparator().compare(a, b)
        except Error as e:
            usage()
    else:
        usage()