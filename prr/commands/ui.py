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

import uvicorn

console = Console(log_time=False, log_path=False)


class UIPromptCommand:
    def __init__(self, args, prompt_args=None):
        self.args = args
        self.prompt_config = None

        if self.args.get("quiet"):
            self.console = Console(file=StringIO())
        else:
            self.console = Console(log_time=False, log_path=False)

    def start(self):
        prompt_path = os.path.abspath(self.args["prompt_path"])

        if os.path.exists(prompt_path) and os.access(prompt_path, os.R_OK):
          self.console.log(f":magnifying_glass_tilted_left: Reading runs of {prompt_path}")
        else:
          raise Exception(f"Cannot read prompt file {prompt_path}")

        # a vital hack
        os.environ["__PRR_WEB_UI_PROMPT_PATH"] = prompt_path

        uvicorn.run("prr.ui:app", host="localhost", port=8400, reload=True, access_log=False)

