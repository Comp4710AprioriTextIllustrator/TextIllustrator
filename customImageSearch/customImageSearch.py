import urllib
import os
import sys
from apiclient.discovery import build

def ensureDirectory(directory):
	if not os.path.exists(directory):
		os.makedirs(directory)

def getFileName(link):
	split = link.rsplit('/', 1 )
	return split[1]
		

service = build("customsearch", "v1",
               developerKey='AIzaSyD-xxBlGIbFjiyADi1VUs-8i1cEKaY8zxw')

			   
searchTerm= sys.argv[1]
saveDirectory= './searchImages/'
ensureDirectory(saveDirectory)

res = service.cse().list(
    q=searchTerm,
    cx='005364439509942707088:ogfepgezvu0',
    searchType='image',
    num=1,
   #imgType='clipart',
    #fileType='png',
    safe= 'off'
).execute()

if not 'items' in res:
    print 'No result !!\nres is: {}'.format(res)
else:
    for item in res['items']:
		#print item['displayLink']
		#print item['link']
		fileName = getFileName(item['link'])
		urllib.urlretrieve( item['link'], saveDirectory + fileName)
		
print 'Done search...image(s) saved in ' + saveDirectory
