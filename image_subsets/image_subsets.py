#!/bin/python
# -*- coding: utf-8 -*-

import image_iterator
import comparators.pixel_comparator
import sys

# Not really sets, since they may contain "duplicate" images(ie ones that when compared return True)
def get_common_subset_of_image_sets(image_subsets, comparator):
    if len(image_subsets) == 0:
        return None
        
    current_image_set = image_subsets[0]
    for image_set in image_subsets[1:]:
        current_image_set = intersection_of_sets(current_image_set, image_set, comparator)
    
    return current_image_set

'''
Performs a block based intersection of the two image sets image_set1 and image_set2 using the comparator specified by the comparator parameter
'''
def intersection_of_sets(image_set1, image_set2, comparator):
    subset = []
    # Done this way so we don't keep more that 2*image_iterator.max_images_per_block
    for images in image_iterator.load_images(image_set1):
        for other_images in image_iterator.load_images(image_set2):
            # Load 2 blocks of images into memory, run a comparison of every image in the first block against all images in the second block.
            for image in images:
                for other_image in other_images:
                    if comparator.compare(image[1], other_image[1]):
                        subset.append(image[0])
                        break
    return subset
    
def parse_subsets(subset_file):
    subsets = []
    curr_subset = []
    curr_line = subset_file.readline()
    while curr_line != '':
        if curr_line.strip() == '' and len(curr_subset) > 0:
            subsets.append(curr_subset)
            curr_subset = []
        elif curr_line.strip() != '':
            curr_subset.append(curr_line.strip())
        
        curr_line = subset_file.readline()
    '''for subset_line in subset_file:
        print subset_line
        curr_line = subset_line.strip()
        if curr_line == '' and len(curr_subset) > 0:
            subsets.append(curr_subset)
            curr_subset = []
            break
            
        curr_subset.append(curr_line)
    '''
    if len(curr_subset) > 0:
        subsets.append(curr_subset)
    return subsets
    
def usage():
    print "python image_subsets.py <image_sets_file>"

'''
Will parse a file were grouped lines of file paths are considered sets of images. Then find the common subset of these sets.
Example:

test_file.txt
-------------

C:\some_file.bmp
C:\some_other_file.bmp

C:\another_file.jpg

C:\final_file.gif

----------------

This will produce 3 sets
1: ['C:\some_file.bmp', 'C:\some_other_file.bmp']
2: ['C:\another_file.jpg']
3: ['C:\final_file.gif']

'''
if __name__=="__main__":
    if len(sys.argv) == 2:
        try:
            image_subsets = None
            with open(sys.argv[1], 'r') as subset_file:
                image_subsets = parse_subsets(subset_file)
            
            print image_subsets
            if image_subsets:
                print get_common_subset_of_image_sets(image_subsets, comparators.pixel_comparator.PixelComparator())
        except Exception as e:
            print e
            usage()
    else:
        usage()