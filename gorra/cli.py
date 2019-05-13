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
import threading

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
    targets=[]
    logging.basicConfig(filename=ctx.config["log_file"],\
    level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")
    logfile=ctx.config["log_file"]

    alarma.send("starting monitor")
    for chain in ctx.config["targets"]:
        target_bp=target.Target(chain,ctx.config["targets"][chain]["max_time_last_block"])
        targets.append(target_bp)
        endpoint=ctx.config["targets"][chain]["endpoint"]
        path=endpoint+ctx.config["targets"][chain]["path"]
        expected_response=ctx.config["targets"][chain]["response"]
        try:
            threading.Thread(target=check_endpoint,args=(path,expected_response,logfile,target_bp,endpoint)).start()
        except Exception as e:
            print("cant start thread")
            print(e)
            continue

def check_endpoint(path,expected_response,logfile,target_bp,endpoint):
    while True:
        with threading.Lock():
            print("#################")
            print("path= ",path)
            print("expected_response: ",expected_response)
            print("logfile: ",logfile)
            print("target_bp: ",target_bp.name)
            print("endpoint: ",endpoint)
        try:
            time.sleep(0.5)
            url_check=url.check_url(path,expected_response,logfile)
            if not url_check:
                alarma.send("Connection problems with the API: "+\
                endpoint+", you should check")
                time.sleep(5)
                continue
            
            bp_check=eos.check(target_bp,logfile,endpoint)

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
        except Exception as e:
            print("Exception: ")
            print(e)
            time.sleep(2)
            continue
