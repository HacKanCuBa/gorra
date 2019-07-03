import sys
import requests
import time
import logging


def check_url(target,esperado,log_file):
    logging.basicConfig(filename=log_file,level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")

    try:
        r=requests.get(target, timeout=40)
        status=str(r.status_code)
        if status  in  esperado:
            return True
        else:
            return False
    except requests.exceptions.ConnectionError:
        return False
