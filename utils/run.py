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

class RunPromptCommand():
  def __init__(self, args):
    self.args = args

    print(args)

    self.prompt = None
    self.config = None

    self.load_prompt_for_path()
    self.load_config_for_prompt()

    self.runner = Runner(self.prompt, self.config)

  def full_model_name_description_from_config(self, model_config):
    model_provider_name = "/".join([model_config['provider_name'], model_config['model_name']])

    if model_config['model_config_name'] and model_provider_name != model_config['model_config_name']:
      return f"{model_config['model_config_name']} ({model_provider_name})"

    return model_provider_name

  def print_run_results(self, result, run_save_directory):
    prompt = result.prompt
    response = result.response

    if self.args['abbrev']:
      console.log("Prompt:      " + "[yellow]" + prompt.text_abbrev(25) + f"[/yellow] ({prompt.text_len()} chars)")
      console.log("Completion:  " + "[green]" + response.completion_abbrev(25) + f"[/green] ({response.completion_len()} chars)")
    else:
      console.log(Panel('[yellow]' + prompt.text() + '[/yellow]'))
      console.log(Panel('[green]' + response.completion + '[/green]'))

    completion = f"[blue]Completion length[/blue]: {response.completion_len()} bytes"
    tokens_used = f"[blue]Tokens used[/blue]: {response.tokens_used}"
    elapsed_time = f"[blue]Elapsed time[/blue]: {round(result.elapsed_time, 2)}s"

    console.log(f"{completion} {tokens_used} {elapsed_time}")

    if run_save_directory:
      console.log(f"💾 {run_save_directory}")

  def run_prompt_model_with_config(self, model_config_name, save=False):
    model_config = self.config.model(model_config_name)
    model_description = self.full_model_name_description_from_config(model_config)

    with console.status(f":robot: [bold green]{model_description}[/bold green]") as status:
      options = self.runner.model_options_for_model(model_config_name)

      console.log(f"\n🤖 [bold]{model_description}[/bold] {options.description()}", style="frame")

      status.update(status="running model", spinner="dots8Bit")

      result, run_save_directory = self.runner.run_model(model_config_name, save)

      self.print_run_results(result, run_save_directory)


  def load_config_for_prompt(self):
    config_loader = ConfigLoader(self.prompt)
    default_model = self.args['model']

    if config_loader.config_file_exists():
      console.log(f":thumbs_up: Using config: {config_loader.config_path}")
      self.config = config_loader.load()
    else:
      console.log(f":x: No config found for the prompt, will use default values")

      if not default_model:
        console.log(f":white_flag: No model specified with DEFAULT_MODEL variable (see .env.example) and no --model option provided, giving up.")
        exit(-1)

      self.config = config_loader.from_dict({
        "models": [
          default_model
        ]
      })

      console.log(f"✅ Will run {default_model} as a default.")

  def load_prompt_for_path(self):
    prompt_path = self.args['prompt_path']

    if not os.path.exists(prompt_path) or not os.access(prompt_path, os.R_OK):
      console.log(f":x: Prompt file {prompt_path} is not accessible, giving up.")
      exit(-1)

    console.log(f":magnifying_glass_tilted_left: Reading {prompt_path}")
    prompt_loader = PromptLoader(prompt_path)
    self.prompt = prompt_loader.load()

  def run_prompt(self):
    models_to_run = self.runner.configured_models()

    console.log(f":racing_car:  Models to run: {models_to_run}")

    if not self.args["abbrev"]:
      print(Panel(self.prompt.text()))

    for model_config_name in models_to_run:
      self.run_prompt_model_with_config(model_config_name, self.args['save'])