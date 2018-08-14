# index_module
purpose:
  To be used in a web-scraping scripts for keeping index of already downloaded files/links.
  
Usage: 
	import: from Index_handler import Index_handler
	initialize: index = Index_handler.Index(param1, param2)
	params: TWO params both OPTIONAL
		- param1: file='index.index' = the name of the file you need created
			By default it will be created in the dir&name of your script with, 
			if you want some other dir for some reson give it full path
		- param2: limit=100 = this will limit the index file size (rows of entries) 
			with the number you want by deleting the older entries

sample code:
  ind = Index_handler.Index(file='index.index', limit=10)
  for url in (urls):
      if ind.check(url):
          ind.write(url)
  ind.save()

How it works:
  works with 3 callable functions: 

  check() accepts one argument - url/md5hash/any-string checks if the string exists in our index file
      check("https://www.drupal.org/docs/develop") # returns true if url does NOT exist

  write() Write all the urls that passed the check functon with True,
      creates a dictionary with this urls and time of saving:
      {"https://www.drupal.org": "2018-08-11-14:33"}
      the reason we need this dict is to avoid duplicated urls
      whithin the same run of the webdownloading process
      If the user proveds only a url we also put the current date as a value to the url key.
  
  save() no params
    This is the function that write in the index file, it's called at the end
		of the downloading process so we only write once, saving some time.
