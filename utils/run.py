#!/usr/bin/env python3.10

DEFAULT_MODEL = "openai/gpt-3.5-turbo"

import sys
sys.path.append('.')
sys.path.append('/opt/conda/lib/python3.10/site-packages')

import argparse

from dotenv import load_dotenv
load_dotenv()

from lib.library import Library
from lib.runner import Runner

parser = argparse.ArgumentParser(description="Run a prompt against a model.",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('--abbrev', help="Abbreviate prompts and completions", action=argparse.BooleanOptionalAction, default=True)
parser.add_argument("--full_completions", "-fc", help="Display full completions with no abbreviating", default=False)
parser.add_argument("prompt_path", help="Path to prompt to run")
args = parser.parse_args()
parsed_args = vars(args)

prompt_path = parsed_args["prompt_path"]
abbrev = parsed_args["abbrev"]

library = Library("prompts")

prompt, config = library.get_prompt_and_config(prompt_path)

runner = Runner(prompt, config)

results = runner.run_all_configured_models()

for model in results.keys():
  result = results[model]
  print("\n")
  print(result.description(abbrev))