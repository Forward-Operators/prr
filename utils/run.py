#!/usr/bin/env python3.10

import os
import sys

sys.path.append('.')
sys.path.append('/opt/conda/lib/python3.10/site-packages')

from dotenv import load_dotenv
load_dotenv()

from rich import print
from rich.console import Console
from rich.panel import Panel

from lib.prompts.loader import PromptLoader
from lib.runs.config import ConfigLoader
from lib.runs.runner import Runner

console = Console(log_time=False, log_path=False)

def full_model_name_description_from_config(model_config):
  model_provider_name = "/".join([model_config['provider_name'], model_config['model_name']])

  if model_config['model_config_name'] and model_provider_name != model_config['model_config_name']:
    return f"{model_config['model_config_name']} ({model_provider_name})"

  return model_provider_name


def run_prompt_model_with_args_and_config(parsed_args, model_config_name, runner):
  model_config = runner.config.model(model_config_name)
  model_description = full_model_name_description_from_config(model_config)

  with console.status(f":robot: [bold green]{model_description}[/bold green]") as status:
    options = runner.model_options_for_model(model_config_name)

    console.print(f"\n🤖 [bold]{model_description}[/bold] {options.description()}", style="frame")

    status.update(status="[bold red]Moving Covid32.exe to Trash", spinner="bouncingBall", spinner_style="yellow")

    result, run_save_directory = runner.run_model(model_config_name)

    if parsed_args['abbrev']:
      console.log("Prompt:      " + "[yellow]" + result.prompt.text_abbrev(25) + f"[/yellow] ({result.prompt.text_len()} chars)")
      console.log("Completion:  " + "[green]" + result.response.completion_abbrev(25) + f"[/green] ({result.response.completion_len()} chars)")
    else:
      console.log(Panel('[yellow]' + result.prompt.text() + '[/yellow]'))
      console.log(Panel('[green]' + result.response.completion + '[/green]'))

    completion = f"[blue]Completion length[/blue]: {result.response.completion_len()} bytes"
    tokens_used = f"[blue]Tokens used[/blue]: {result.response.tokens_used}"
    elapsed_time = f"[blue]Elapsed time[/blue]: {round(result.elapsed_time, 2)}s"

    console.log(f"{completion} {tokens_used} {elapsed_time}")

    console.log(f"💾 {run_save_directory}")


def load_config_for_prompt(prompt, default_model=None):
  config_loader = ConfigLoader(prompt)

  if config_loader.config_file_exists():
    console.log(f":thumbs_up: Using config: {config_loader.config_path}")
    config = config_loader.load()
  else:
    console.log(f":x: No config found for the prompt, will use default values")

    if not default_model:
      console.log(f":white_flag: No model specified with DEFAULT_MODEL variable (see .env.example) and no --model option provided, giving up.")
      exit(-1)

    config = config_loader.from_dict({
      "models": [
        default_model
      ]
    })

    console.log(f"✅ Will run {default_model} as a default.")

  return config

def load_prompt_for_path(prompt_path):
  prompt_loader = PromptLoader(prompt_path)
  prompt = prompt_loader.load()

  return prompt

def run_prompt_with_args(parsed_args):
  prompt_path = parsed_args["prompt_path"]
  default_model = parsed_args["model"]

  prompt = load_prompt_for_path(prompt_path)
  console.log(f":magnifying_glass_tilted_left: Reading {prompt.text_len()} bytes of prompt from {prompt_path}")

  config = load_config_for_prompt(prompt, default_model)

  runner = Runner(prompt, config)
  models_to_run = runner.configured_models()

  console.log(f"🏎️ Models to run: {models_to_run}")

  if not parsed_args["abbrev"]:
    print(Panel(prompt.text()))

  for model_config_name in models_to_run:
    run_prompt_model_with_args_and_config(parsed_args, runner, model_config_name)