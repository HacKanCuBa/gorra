import sys
import requests
import time
import logging


def check_url(target,esperado):
	logging.basicConfig(filename="/var/log/gorra.log",level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")

	try:
		r=requests.get(target)
		status=str(r.status_code)
		if status  in  esperado:
			return True
		else:
			return False
	except Exception as e:
		logging.info("get_info", e)
