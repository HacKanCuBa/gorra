import sys
import requests
import yaml
import time
from modules import eos, url
from . import target
import click
from functools import update_wrapper
import logging


@click.group()
@click.option(
    "--configfile",
    default="config.yml",
)
@click.pass_context
def main(ctx, **kwargs):
	ctx.obj = {}
	for k, v in kwargs.items():
		ctx.obj[k] = v


def config(f):
    @click.pass_context
    def new_func(ctx, *args, **kwargs):
        ctx.config = yaml.safe_load(open(ctx.obj["configfile"]))
        return ctx.invoke(f, *args, **kwargs)
    return update_wrapper(new_func, f)


@main.command()
@config
@click.pass_context
def monitor(ctx, **kwargs):
	logging.basicConfig(filename=ctx.config["log_file"],level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")
	target_bp=target.Target(ctx.config["eos"]["target"]["name"],ctx.config["eos"]["target"]["max_time_last_block"],ctx.config["eos"]["target"]["stand_by"])

	while True:
		url_check=url.check_url(ctx.config["url_target"]["endpoint"],ctx.config["url_target"]["response"],ctx.config["log_file"])
		if not url_check:
			alarma("your api is not working")
			time.sleep(5)
			continue
		bp_check=eos.check(target_bp,ctx.config["log_file"],ctx.config["url_target"]["endpoint"])
		if not bp_check:
			if bp_check == "upgrade":
				alarma("you are top 21 now")
				logging.info("you are top 21 now :)")
			elif bp_check =="downgrade":
				alarma("you are standby now :(")
				logging.info("you are standby now :( ")
			else:
				alarma("you are missing blocks")
				logging.info("you are missing blocks")


#TODO meterlo en un modulo y ponerle twilio y otras alarmas.
def alarma(bot_message):
	print(bot_message)
	# logging.info(bot_message)
	send_text = 'https://api.telegram.org/bot' + ctx.config["t_bot"]["bot_token"] + '/sendMessage?chat_id=' + ctx.config["t_bot"]["chat_id"] + '&parse_mode=Markdown&text=' + bot_message
	# requests.get(send_text)
