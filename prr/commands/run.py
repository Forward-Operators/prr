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

console = Console(log_time=False, log_path=False)


class RunPromptCommand:
    def __init__(self, args, prompt_args=None):
        self.args = args
        self.prompt_args = prompt_args
        self.prompt_config = None

        if self.args["quiet"]:
            self.console = Console(file=StringIO())
        else:
            self.console = Console(log_time=False, log_path=False)

        if self.args["log"]:
            self.save_run = True
        else:
            self.save_run = False

        self.load_prompt_for_path()
        self.runner = Runner(self.prompt_config, self.save_run, self.prompt_args)

    def print_prompt(self, request):
        if self.args["abbrev"]:
            self.console.log(
                "Prompt:      "
                + "[yellow]"
                + request.prompt_text(25).strip()
                + f"[/yellow] ({len(request.prompt_text())} chars)"
            )
        else:
            self.console.log(
                Panel("[yellow]" + request.prompt_text().strip() + "[/yellow]")
            )

    def print_completion(self, response):
        if self.args["abbrev"]:
            self.console.log(
                "Completion:  "
                + "[green]"
                + response.response_text(25).strip()
                + f"[/green] ({len(response.response_content)} chars)"
            )
        else:
            self.console.log(
                Panel("[green]" + str(response.response_text()).strip() + "[/green]")
            )

    def print_basic_stats(self, result):
        response = result.response

        completion = (
            f"[blue]Completion length[/blue]: {len(response.response_content)} bytes"
        )
        tokens_used = f"[blue]Tokens used[/blue]: {response.tokens_used()}"
        elapsed_time = f"[blue]Elapsed time[/blue]: {round(result.elapsed_time, 2)}s"

        self.console.log(f"{completion} {tokens_used} {elapsed_time}")

    def print_run_parameters(self, service_name, request):
        self.console.log(
            f"🤖 [magenta]{service_name}[/magenta] {request.options.description()}",
            style="frame",
        )

    def print_run_results(self, result, run_save_directory):
        request = result.request
        response = result.response

        if self.args["quiet"]:
            # just print out the output verbatim
            if isinstance(response.response_content, str):
                print(response.response_content)
            else:
                sys.stdout.buffer.write(response.response_content)
        else:
            self.print_completion(response)
            self.print_basic_stats(result)

            if run_save_directory:
                self.console.log(f"💾 {run_save_directory}")
                self.console.log("")

    def on_request(self, service_name, request):
        self.print_run_parameters(service_name, request)
        self.print_prompt(request)

    def load_prompt_for_path(self):
        prompt_path = self.args["prompt_path"]

        self.console.log(f":magnifying_glass_tilted_left: Reading {prompt_path}")

        loader = PromptConfigLoader()
        self.prompt_config = loader.load_from_path(prompt_path)

    def services_to_run(self):
        _services = self.prompt_config.configured_services()

        if _services == []:
            if self.args["service"]:
                _services = [self.args["service"]]
                self.console.log(
                    f":racing_car:  Running service {self.args['service']}."
                )
            else:
                self.console.log(
                    f":x: No services configured for prompt {self.args['prompt_path']}, in ~/.prr_rc nor given in command-line."
                )
                exit(-1)
        else:
            self.console.log(f":racing_car:  Running services: {_services}")

        return _services

    def run_prompt(self):
        services = self.services_to_run()

        self.runner.run_services(
            services,
            self.args,
            {
                "on_request": lambda service_name, request: self.on_request(
                    service_name, request
                ),
                "on_result": lambda service_name, result, run_save_directory: self.print_run_results(
                    result, run_save_directory
                ),
            },
        )
