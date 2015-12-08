#!/bin/python
# -*- coding: utf-8 -*-

import math
import sys

from PIL import Image

class AvgPixelsComparator(object):
    # Want to be able to tighten or loosen the comparison constraints 
    def __init__(self, num_kernels_horizontal=2, num_kernels_vertical=2, avg_comparator=lambda x, y: x == y):
        # This is an approximate number of kernels
        self.__num_kernels_horizontal = num_kernels_horizontal
        self.__num_kernels_vertical = num_kernels_vertical
        self.__avg_comparator = avg_comparator

    def compare(self, image1, image2):
        # Algorithm won't work if any dimension doesn't satisfy the following conditions num_pixels < num_kernels + 2
        if image1.width < self.__num_kernels_horizontal + 2 or image2.width < self.__num_kernels_horizontal + 2:
            raise ValueError("Error: The heights of the provided images ({image1width}, {image2width}) are not greater than or equal to the requested number of kernels ({num_kernels} + 2)".format(image1width=image1.width, image2width=image2.width, num_kernels=self.__num_kernels_horizontal))
            
        if image1.height < self.__num_kernels_vertical + 2 or image2.height < self.__num_kernels_vertical + 2:
            raise ValueError("Error: The heights of the provided images ({image1height}, {image2height}) are not greater than or equal to the requested number of kernels ({num_kernels} + 2)".format(image1height=image1.height, image2height=image2.height, num_kernels=self.__num_kernels_vertical))
    
        image1_kernel_width = self.__calc_dimension(image1.width, self.__num_kernels_horizontal)
        image1_kernel_height = self.__calc_dimension(image1.height, self.__num_kernels_vertical)
        image1_kernel_horizontal_move_amt = self.__calc_move_amount(image1.width, self.__num_kernels_horizontal)
        image1_kernel_vertical_move_amt = self.__calc_move_amount(image1.height, self.__num_kernels_vertical)
        
        image2_kernel_width = self.__calc_dimension(image2.width, self.__num_kernels_horizontal)
        image2_kernel_height = self.__calc_dimension(image2.height, self.__num_kernels_vertical)
        image2_kernel_horizontal_move_amt = self.__calc_move_amount(image2.width, self.__num_kernels_horizontal)
        image2_kernel_vertical_move_amt = self.__calc_move_amount(image2.height, self.__num_kernels_vertical)
        
        same_image = True
        image1_x = 0.0
        image2_x = 0.0
        for x_kernel in range(self.__num_kernels_horizontal):
            image1_y = 0.0
            image2_y = 0.0
            for y_kernel in range(self.__num_kernels_vertical):
                kernel_avg_image1 = self.__get_colour_avg_of_kernel(image1_x, image1_y, image1_kernel_width, image1_kernel_height, image1)
                kernel_avg_image2 = self.__get_colour_avg_of_kernel(image2_x, image2_y, image2_kernel_width, image2_kernel_height, image2)
                
                image1_y += image1_kernel_vertical_move_amt
                image2_y += image2_kernel_vertical_move_amt
                print kernel_avg_image1, kernel_avg_image2
                if not self.__avg_comparator(kernel_avg_image1, kernel_avg_image2):
                    same_image = False
                    break
            image1_x += image1_kernel_horizontal_move_amt
            image2_x += image2_kernel_horizontal_move_amt
            if not same_image:
                break
        
        return same_image
        
    def __calc_dimension(self, image_dimension, num_kernels_on_dimension):
        # Includes extra pixel below and above the core kernel
        return int(math.floor(float(image_dimension)/num_kernels_on_dimension))
        
    def __calc_move_amount(self, image_dimension, num_kernels_on_dimension):
        return float(image_dimension)/num_kernels_on_dimension
        
    def __get_colour_avg_of_kernel(self, kernel_x, kernel_y, kernel_width, kernel_height, image):
        pixel_sum = 0
        print "New Kernel"
        for i in range(kernel_width):
            for j in range(kernel_height):
                print kernel_x, kernel_y, i, j, image.getpixel((int(kernel_x) + i, int(kernel_y) + j))
                pixel_sum += image.getpixel((int(kernel_x) + i, int(kernel_y) + j))
        return pixel_sum / float(kernel_width * kernel_height)
            
    
def usage():
    print "python avg_pixel_comparator.py <image_1> <image_2>"
    
if __name__=="__main__":
    if len(sys.argv) == 3:
        try:
            comparator = AvgPixelsComparator()
            image1 = Image.open(sys.argv[1])
            image2 = Image.open(sys.argv[2])
            
            print comparator.compare(image1, image2)
        except Exception as e:
            print e
            print usage()
    else:
        usage()