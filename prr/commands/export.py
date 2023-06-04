#!/usr/bin/env python

import os
import sys
from io import StringIO

from rich import print
from rich.console import Console
from rich.panel import Panel

from prr.prompt import Prompt
from prr.prompt.prompt_loader import PromptConfigLoader
from prr.runner import Runner
from prr.runner.saved_run import SavedRunsCollection

console = Console(log_time=False, log_path=False)


class ExportPromptCommand:
    def __init__(self, args, prompt_args=None):
        self.args = args
        self.prompt_config = None

        if self.args.get("quiet"):
            self.console = Console(file=StringIO())
        else:
            self.console = Console(log_time=False, log_path=False)

        self.saved_runs_collection()

        self.export_prompt()

    def saved_runs_collection(self):
        prompt_path = self.args["prompt_path"]

        self.console.log(f":magnifying_glass_tilted_left: Reading runs of {prompt_path}")

        self.collection = SavedRunsCollection(prompt_path)

    def export_prompt(self):
        runs = self.collection.all()

        for run in runs:
          print("---- run", run.id())
          services = run.services()

          for service in services:
            print("---- service", service.name())
            print("-------- prompt_content")
            print(service.prompt_content())
            print("-------- output_content")
            print(service.output_content())
            print("-------- run_details")
            print(service.run_details())
