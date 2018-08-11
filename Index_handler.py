'''
PANDORA Indexing module

author: tvalov

Usage: 
	from Index_handler import Index_handler
	initialize: index = Index_handler.Index(param1, param2)
		params: TWO params both OPTIONAL
			- param1: file='index.index' = the name of the file you need created
				By default it will be created in the dir&name of your script with, 
				if you want some other dir for some reson give it full path
			- param2: limit=100 = this will limit the index file size 
				with the number you want by deleting the older entries
    check if a given url is in the index with check(url): 
    	if ind.check(url): 
			this will return True || False
	then use write(url) to temporarely store the url in an array of dict
        	ind.write(url)
	finally you can call save() to save/write the temporarily stored urls
		ind.save()
'''
import os
import sys
import re
import datetime
import time

script_dir, filename = os.path.split(os.path.abspath(sys.argv[0]))
file = os.path.splitext(filename)[0]
data_dir = re.sub(r'\/bin\/', '/data/', script_dir, flags=re.I|re.S)
defeult_index = "{}.index".format(os.path.join(data_dir, file))


class Index:
	'''
	Main and only class responsible for everything
	'''
	def __init__(self, **kwargs):
		self.index_file = kwargs.get('file', defeult_index)
		self.limit = kwargs.get('limit', None)
		self.index_content = self.read_index()
		# take the number of lines and check against limitation
		self.num_lines = sum(1 for key in self.index_content)
		if self.num_lines >= self.limit:
			self.limitation()

	def read_index(self):
		'''
		Read the index file, if there is no index file create one and return empty array
		if there is no index file givven as a param look for a file called index.index
		situated in the directory of the script that calls the module
		'''
		if os.path.exists(self.index_file):
			with open(self.index_file, 'r') as f:
				content_arr = []
				for line in f.readlines():
					key, value = [i.rstrip() for i in line.split('\t', 1)]
					content_arr.append(dict({key:value}))
				return content_arr
		else:
			print("Creating index file with name: {}".format(defeult_index))
			return []

	def check(self, url):
		'''
		here we check if the url is unique, comparing it to what is already in the index
		'''
		if len([el for el in self.index_content if url in el]) > 0:
			return False

		return True

	def write(self, url, option=datetime.datetime.now().strftime('%Y-%m-%d-%H:%M')):
		'''
		Write all the urls that passed the check functon with True,
		the reason we need this dict is to avoid duplicated urls
		whithin the same run of the webdownloading process
		If the user proveds only a url we also put the current date as a value to the url key
		'''
		self.index_content.append(dict({url:option}))

	def save(self):
		'''
		This is the function that write in the index file, it's called at the end
		of the downloading process so we only write once
		'''
		with open(self.index_file, "w") as f:
			for elm in self.index_content:
				for key, val in elm.items():
					f.write("{}\t{}\n".format(key, val))

	def limitation(self):
		'''
		This functionality is optional it limits the size of the index file
		'''
		del self.index_content[:self.limit]
		self.save()
