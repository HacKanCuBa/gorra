import sys
import requests
import yaml
import time
from modules import eos, url, alarma
from modules.alarma import Alarma
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
	alarma =Alarma(ctx)
	logging.basicConfig(filename=ctx.config["log_file"],level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")
    
	#target_bp=target.Target(ctx.config["eos"]["target"]["name"],ctx.config["eos"]["target"]["max_time_last_block"])

	while True:
		try:
			time.sleep(0.5)
			for chain in ctx.config["targets"]:

				endpoint=ctx.config["targets"][chain]["endpoint"]
				url=endpoint+ctx.config["targets"][chain]["path"]
				expected_response=ctx.config["targets"][chain]["response"]
				

				url_check=url.check_url(url,expected_response,ctx.config["log_file"])
				if not url_check:
					alarma.send("Connection problems with the API, you should check")
					time.sleep(5)
					continue
				
				bp_check=eos.check(target_bp,ctx.config["log_file"],ctx.config["url_target"]["endpoint"])

				if bp_check != True:
					if bp_check == "upgrade":
						alarma.send("you are top 21 now :)")
						logging.info("you are top 21 now :)")
					elif bp_check == "downgrade":
						alarma.send("you are standby now :(")
						logging.info("you are standby now :( ")
					else:
						alarma.send("you are missing blocks")
						logging.info("you are missing blocks")
						time.sleep(5)
		except:
			time.sleep(2)
			continue


		
