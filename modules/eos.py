import sys
import yaml
import requests
import os
import sys
import time
import json
from subprocess import check_output
import logging


def check(producer):
    #check if upgrade
    logging.basicConfig(filename="/var/log/gorra.log",level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")
	if producer.stand_by:
		top=get_current_top()
		if producer.name in top:
			producer.stand_by=False
			return "upgrade"
		else:
			return True
	prod=get_current_producer()
	if producer.name == prod:
		producer.last_block_time=time.time()
		return True
	elif time.time() - producer.last_block_time > producer.max_time_last_block:
		if is_producer(producer.name):
			return False
		else:
			producer.last_block_time=time.time()
			return True
	else:
		return True

def get_current_producer():
	#TODO: remove hardcoding
	r=requests.get('https://api.eosargentina.io/v1/chain/get_info')
	return str(r.json()["head_block_producer"])

def is_producer(producer):
	if producer in get_current_top():
		return True
	else:
		return False

def get_current_top():
	#TODO: remove hardcoding
	top=[]
	payload= "{\"limit\":\"21\",\"json\":\"true\"}"
	api="https://api.eosargentina.io/"
	r=requests.post(api+"v1/chain/get_producers", data =payload)
	for bp in r.json()["rows"]:
		top.append(bp["owner"])
	return top
