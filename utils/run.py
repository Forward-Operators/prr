#!/usr/bin/env python3.10

import sys
import time

sys.path.append('.')
sys.path.append('/opt/conda/lib/python3.10/site-packages')

import argparse

from dotenv import load_dotenv
load_dotenv()

from rich.console import Console

from lib.prompts.library import Library
from lib.runs.runner import Runner

console = Console(log_time=True, log_path=False)

parser = argparse.ArgumentParser(description="Run a prompt against configured models.",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('--quiet', '-q', help="Disable any stdout output", default=False)
parser.add_argument('--verbose', '-v', help="Be verbose and explain each step", default=False)
parser.add_argument('--library', '-l', help="Path to prompt library directory", default="./prompts")
parser.add_argument('--abbrev', help="Abbreviate prompts and completions", action=argparse.BooleanOptionalAction, default=True)
parser.add_argument("--full_completions", "-fc", help="Display full completions with no abbreviating", default=False)
parser.add_argument("prompt_path", help="Path to prompt to run")
args = parser.parse_args()
parsed_args = vars(args)

prompt_path = parsed_args["prompt_path"]
abbrev = parsed_args["abbrev"]
library_path = parsed_args["library"]
quiet = parsed_args["quiet"]

console.log(f":books: Using prompt library at: {library_path}")
library = Library(library_path)

console.log(f":magnifying_glass_tilted_left: Looking up prompt: {prompt_path}")
prompt, config = library.get_prompt_and_config(prompt_path)
console.log(f":magnifying_glass_tilted_left: Prompt found: {prompt.path}")

if not config or config.empty():
  console.error(f":x: No config found for: {prompt.path}")
  sys.exit(-1)

console.log(f"Config found for: {config.models()}")

runner = Runner(prompt, config)

for model in runner.configured_models():
  with console.status(f":robot: [bold green]{model}") as status:
    console.log(f"{model} run started")
    result, run_save_directory = runner.run_model(model)
    print(result.description(abbrev))
    console.log(f"{model} run done complete, saved to {run_save_directory}")