import sys
import yaml
import requests
import os
import sys
import time
import json
from subprocess import check_output
import logging


def check(producer,log_file,api):
    logging.basicConfig(filename=log_file,level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")
    top=get_current_top(api)
    #set stand_by
    if producer.stand_by == None:
        if is_producer(producer.name,api):
            print("producer in schedule: ",producer.name)
            producer.stand_by=False
        else:
            print("producer stand by: ",producer.name)
            producer.stand_by=True

    if is_producer(producer.name,api):
        #check if upgrade
        if producer.stand_by==True:
            producer.stand_by=False
            producer.last_block_time=time.time()
            return "upgrade"
        else:
            #check missing blocks
            prod=get_current_producer(api)
            if producer.name == prod:
                producer.last_block_time=time.time()
                return True
            elif time.time() - producer.last_block_time > producer.max_time_last_block:
                return False
            else:
                return True
    else:
        #check if downgrade
        if producer.stand_by==False:
            producer.stand_by=True
            return "downgrade"
        else:
            return True



def get_current_producer(api):
    #TODO: remove hardcoding
    r=requests.get(api+'/v1/chain/get_info')
    return str(r.json()["head_block_producer"])

def is_producer(producer,api):
    if producer in get_current_top(api):
        return True
    else:
        return False

def get_current_top(api):
    #TODO: remove hardcoding
    top=[]
    payload= "{\"limit\":\"21\",\"json\":\"true\"}"
    r=requests.post(api+"/v1/chain/get_producer_schedule", data =payload)
    for bp in r.json()["active"]["producers"]:
        top.append(bp["producer_name"])
    return top
