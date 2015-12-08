# TextIllustrator
## Installing Dependencies
Dependencies are installed using pip. Installation instructions for pip can be found [here](https://pip.readthedocs.org/en/stable/installing)
```
pip install scrapy
pip install pillow
pip install pymongo
```

## Running a spider
Example:

Note: Assumes that you start in base directory of project
```
cd datacollecter
scrapy crawl bbc
```

## Instructions
1) use a spider or spiders to populate the database collection text_illustrator.articles with as much articles as you feel want
2) for each language. choose a set of sites that represent a language and run:
```
language_model = generate_model(sites, language_name, settings)
```
3) for each article or set of articles of your chouse, run
```
word_sets = salient_sets(article_set)
```
4) Download images for word sets...

5) Find common subsets of images
```
image_sets = [image_set, image_set, ..., image_set]
common_image_subset = get_common_subset_of_image_sets(image_sets, comparator)
````
Note: 
* image_set is a set of file paths to the downloaded images
* comparator should be a chained comparator at least both a pixel comparator and average pixel comparator in the chain


5) Convert word sets into a set of illustrations
