#!/usr/bin/env python3.10

import os
import sys

sys.path.append('.')
sys.path.append('/opt/conda/lib/python3.10/site-packages')

import argparse
from dotenv import load_dotenv
load_dotenv()

from rich import print
from rich.console import Console
from rich.panel import Panel

from lib.prompts.loader import PromptLoader
from lib.runs.config import ConfigLoader
from lib.runs.runner import Runner

console = Console(log_time=False, log_path=False)

parser = argparse.ArgumentParser(description="Run a prompt against configured models.",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('--quiet', '-q', help="Disable any stdout output", default=False)
parser.add_argument('--verbose', '-v', help="Be verbose and explain each step", default=False)
parser.add_argument('--abbrev', help="Abbreviate prompts and completions", action=argparse.BooleanOptionalAction, default=True)
parser.add_argument("--model", "-m", help="Model to use if none is configured (defaults to DEFAULT_MODEL environment variable)", default=os.environ.get('DEFAULT_MODEL'))
parser.add_argument("prompt_path", help="Path to prompt to run")
args = parser.parse_args()
parsed_args = vars(args)

prompt_path = parsed_args["prompt_path"]
abbrev = parsed_args["abbrev"]
quiet = parsed_args["quiet"]
model = parsed_args["model"]

prompt = PromptLoader(prompt_path).load()
config_loader = ConfigLoader(prompt)
config = config_loader.load()

console.log(f":magnifying_glass_tilted_left: Reading {prompt.text_len()} bytes of prompt from {prompt_path}")

config_found = False

if not config or config.empty():
  console.log(f":x: No config found for the prompt, will use default values")

  if not model:
    console.log(f":x: No model specified with DEFAULT_MODEL variable (see .env.example) and no --model option provided, giving up.")
    exit(-1)

  config = config_loader.from_dict({
    "models": [
      model
    ]
  })
  console.log(f"✅ Will run {model} as a default.")
else:
  config_found = True
  console.log(f":magnifying_glass_tilted_left: Using config: {config_loader.config_path}")

runner = Runner(prompt, config)
models_to_run = runner.configured_models()

if config_found:
  console.log(f"✅ Config found for: {models_to_run}")

if not abbrev:
  console.log(f"Prompt:")
  print(Panel(prompt.text()))

for model in models_to_run:
  model_config = runner.config.model(model)

  model_provider_name = "/".join([model_config['provider_name'], model_config['model_name']])

  if model_config['model_config_name'] and model_provider_name != model_config['model_config_name']:
    model_description = f"{model_config['model_config_name']} ({model_provider_name})"
  else:
    model_description = model_provider_name

  with console.status(f":robot: [bold green]{model_description}[/bold green]") as status:
    options = runner.model_options_for_model(model)

    console.print(f"\n🤖 [bold]{model_description}[/bold] {options.description()}", style="frame")

    result, run_save_directory = runner.run_model(model)

    if abbrev:
      console.log(result.description(abbrev))
    else:
      console.log("\nFull completion text:")
      console.log(Panel('[green]' + result.response.completion + '[/green]'))

    console.log(f"💾 run saved to: ")
    console.log(run_save_directory)
    console.log("\n")
