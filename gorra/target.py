import sys
import yaml
import requests
import time
import modules

class Target(object):
	domain=""
	name=""
	port=""
	path=""
	name=""
	stand_by=None  

	def __init__(self,name,mtlb):
		self.name=name
		self.last_block_time=time.time()
		self.max_time_last_block=mtlb
