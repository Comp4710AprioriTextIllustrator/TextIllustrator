#!/bin/python
# -*- coding: utf-8 -*-

import sys

from PIL import Image

max_images_per_block = 50
       
def load_images(image_files):
    for i in range(0, len(image_files), max_images_per_block):
        images = []
        for image_file_path in image_files[i:i+max_images_per_block]:
            try:
                images.append((image_file_path, Image.open(image_file_path)))
            except Exception as e:
                print "Error: Could not open {file} due to {exception}".format(file=image_file_path, exception=str(e))
        yield images
        
def usage():
    print "python image_iterator.py <image1> <image2> ... <imageN>"
        
if __name__=="__main__":
    if len(sys.argv) > 1:
        max_images_per_block = 2
        for images in load_images(sys.argv[1:]):
            print "Loading {num_imgs} images.".format(num_imgs=len(images))
    else:
        usage()