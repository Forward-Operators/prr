#!/usr/bin/env python3.10

DEFAULT_MODEL = "openai/gpt-3.5-turbo"

import sys
sys.path.append('.')
sys.path.append('/opt/conda/lib/python3.10/site-packages')

import argparse

from dotenv import load_dotenv
load_dotenv()

from lib.prompt.library import Library
from lib.runner import Runner

parser = argparse.ArgumentParser(description="Run a prompt against a model.",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-m", "--model", help="model to use", default=DEFAULT_MODEL)
# parser.add_argument("-v", "--verbose", action="store_true", help="increase verbosity")
parser.add_argument("prompt_path", help="Path to prompt to run")
args = parser.parse_args()
config = vars(args)

library = Library("prompts")
prompt = library.get(config["prompt_path"])

model = config["model"] or DEFAULT_MODEL
# model = "anthropic/claude-v1"

runner = Runner(prompt, model)
runner.run()

result = runner.get_result()
stats = runner.get_stats()