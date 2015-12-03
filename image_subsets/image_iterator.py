#!/bin/python
# -*- coding: utf-8 -*-

import sys

from PIL import Image

MAX_IMAGES_PER_BLOCK = 50

class ImageIterator(object):
    def __init__(self, max_images_per_block=MAX_IMAGES_PER_BLOCK):
        self.max_images_per_block=max_images_per_block
        
    def load_images(self, image_files):
        for i in range(0, len(image_files), self.max_images_per_block):
            images = []
            for image_file_path in image_files[i:i+self.max_images_per_block]:
                try:
                    images.append(Image.open(image_file_path))
                except Exception as e:
                    print "Error: Could not open {file} due to {exception}".format(file=image_file_path, exception=str(e))
            yield images
        
def usage():
    print "python image_iterator.py <image1> <image2> ... <imageN>"
        
if __name__=="__main__":
    if len(sys.argv) > 1:
        img_iter = ImageIterator(2)
        for images in img_iter.load_images(sys.argv[1:]):
            print "Loading {num_imgs} images.".format(num_imgs=len(images))
    else:
        usage()