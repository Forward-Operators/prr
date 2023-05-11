#!/usr/bin/env python

import os
import sys
from io import StringIO

from rich import print
from rich.console import Console
from rich.panel import Panel

# from prr.config import config
from prr.prompt import Prompt
from prr.runner import Runner

console = Console(log_time=False, log_path=False)


class RunPromptCommand:
    def __init__(self, args, prompt_args=None):
        self.args = args
        self.prompt_args = prompt_args
        self.prompt = None

        if self.args["quiet"]:
            self.console = Console(file=StringIO())
        else:
            self.console = Console(log_time=False, log_path=False)

        self.load_prompt_for_path()
        self.runner = Runner(self.prompt)

    def print_run_results(self, result, run_save_directory):
        request = result.request
        response = result.response

        if self.args["quiet"]:
            print(response.response_content)
        else:
            if self.args["abbrev"]:
                self.console.log(
                    "Prompt:      "
                    + "[yellow]"
                    + request.prompt_text(25).strip()
                    + f"[/yellow] ({len(request.prompt_text())} chars)"
                )
                self.console.log(
                    "Completion:  "
                    + "[green]"
                    + response.response_abbrev(25).strip()
                    + f"[/green] ({len(response.response_content)} chars)"
                )
            else:
                self.console.log(
                    Panel("[yellow]" + request.prompt_text().strip() + "[/yellow]")
                )
                self.console.log(
                    Panel("[green]" + response.response_content.strip() + "[/green]")
                )

                completion = f"[blue]Completion length[/blue]: {len(response.response_content)} bytes"
                tokens_used = f"[blue]Tokens used[/blue]: {response.tokens_used()}"
                elapsed_time = (
                    f"[blue]Elapsed time[/blue]: {round(result.elapsed_time, 2)}s"
                )

            self.console.log(f"{completion} {tokens_used} {elapsed_time}")

            if run_save_directory:
                self.console.log(f"💾 {run_save_directory}")

    def run_prompt_on_service(self, service_name, save=False):
        service_config = self.prompt.config_for_service(service_name)
        options = service_config.options

        with self.console.status(
            f":robot: [bold green]{service_name}[/bold green]"
        ) as status:
            self.console.log(
                f"\n🤖 [bold]{service_name}[/bold] {options.description()}",
                style="frame",
            )

            status.update(status="running model", spinner="dots8Bit")

            result, run_save_directory = self.runner.run_service(service_name, save)

            self.print_run_results(result, run_save_directory)

    def load_prompt_for_path(self):
        prompt_path = self.args["prompt_path"]

        if not os.path.exists(prompt_path) or not os.access(prompt_path, os.R_OK):
            self.console.log(
                f":x: Prompt file {prompt_path} is not accessible, giving up."
            )
            exit(-1)

        self.console.log(f":magnifying_glass_tilted_left: Reading {prompt_path}")
        self.prompt = Prompt(prompt_path, self.prompt_args)

    def run_prompt(self):
        services_to_run = self.prompt.configured_service_names()

        if services_to_run == []:
            if self.args["service"]:
                services_to_run = [self.args["service"]]
                self.console.log(
                    f":racing_car:  Running service {self.args['service']} with default options."
                )
            else:
                self.console.log(
                    f":x: No services configured for prompt {self.args['prompt_path']}, nor given in command-line. Not even in .env!"
                )
                exit(-1)
        else:
            self.console.log(f":racing_car:  Running services: {services_to_run}")

        if not self.args["abbrev"]:
            self.console.log(Panel(self.prompt.text()))

            for service_name in services_to_run:
                self.run_prompt_on_service(service_name, self.args["log"])
