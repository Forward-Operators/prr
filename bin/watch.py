#!/usr/bin/env python3.10

import os
import sys
import time
import subprocess

sys.path.append('.')
sys.path.append('/opt/conda/lib/python3.10/site-packages')

from dotenv import load_dotenv
load_dotenv()

from lib.prompts.loader import PromptLoader
from lib.runs.config import ConfigLoader
from lib.runs.runner import Runner
from run import CommandArgumentParser

parser = CommandArgumentParser()

args = parser.parse_args()
parsed_args = vars(args)

prompt_path = parsed_args["prompt_path"]

print (f"👀 watching for changes on {prompt_path}")

exit(-1)

prompt = PromptLoader(prompt_path).load()
config_loader = ConfigLoader(prompt)
config_path = config_loader.config_path

info_message = f"👀 watching for changes on {prompt_path} and config file"

cooldown  = os.environ.get('WATCH_RERUN_COOLDOWN_SECONDS')

if cooldown != None:
  if int(cooldown) > 0:
    info_message += f" with {cooldown}s cooldown between re-runs."
  else:
    info_message += f" with no cooldown between re-runs."

info_message += f" Press Ctrl+C to exit."

def timestamp_for_file(path):
  if os.path.exists(path):
    return os.path.getmtime(path)

  return 0


files_to_watch = [prompt_path, config_path]
last_timestamps = [timestamp_for_file(path) for path in files_to_watch]

run_script_path = os.path.join(os.path.dirname(__file__), "run")
# TODO/FIXME: this system business and building args again is ugly
params = [run_script_path]

if abbrev:
  params.append('--abbrev')

if model:
  params.append('--model')
  params.append(model)

params.append(prompt_path)

cmdline = (' ').join(params)

print(info_message)

def run():
  print(f'🧨 running {run_script_path} with prompt_path {params}:', cmdline)
  os.system(cmdline)


while True:
  new_timestamps = [timestamp_for_file(path) for path in files_to_watch]

  if new_timestamps != last_timestamps:
    run()

    if cooldown != None:
      if int(cooldown) > 0:
        print(f'{cooldown}s cooldown...')
        time.sleep(int(cooldown))

    last_timestamps = new_timestamps

  time.sleep(0.25)

