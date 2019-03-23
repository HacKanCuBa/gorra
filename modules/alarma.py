import sys
import requests
import time
import logging


class Alarma:
    def __init__(self,ctx):
        self.token=ctx.config["t_bot"]["bot_token"]
        self.chat_id=ctx.config["t_bot"]["chat_id"]

    def send(self,message):
        print(message)
        try:
        	send_text = 'https://api.telegram.org/bot' + self.token + '/sendMessage?chat_id=' + self.chat_id + '&parse_mode=Markdown&text=' + message
        	requests.get(send_text)
        except requests.exceptions.RequestException as e:
        	print(e)