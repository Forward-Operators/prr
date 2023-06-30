#!/usr/bin/env python

import os
from io import StringIO

import uvicorn
from rich.console import Console

console = Console(log_time=False, log_path=False)

DEFAULT_TEMPLATE_PATH = os.path.join(
    os.path.dirname(__file__), "..", "prompt_template.yaml"
)


class UIPromptCommand:
    def __init__(self, args, prompt_args=None):
        self.args = args
        self.prompt_config = None
        self.prompt_path = None

        if self.args.get("quiet"):
            self.console = Console(file=StringIO())
        else:
            self.console = Console(log_time=False, log_path=False)

    def create_default_config(self, prompt_path):
        if os.access(os.path.dirname(prompt_path), os.W_OK):
            self.console.log(
                f":magnifying_glass_tilted_left: {prompt_path} not found, creating it from template"
            )

            with open(prompt_path, "w") as dst:
                with open(DEFAULT_TEMPLATE_PATH, "r") as src:
                    dst.write(src.read())

                    self.prompt_path = prompt_path
        else:
            raise Exception(f"Cannot create prompt file {prompt_path}")

    def prepare_prompt_path(self):
        prompt_path = os.path.abspath(self.args["prompt_path"])

        if not prompt_path.endswith(".yaml"):
            prompt_path = prompt_path + ".yaml"

        if os.path.exists(prompt_path):
            if os.access(prompt_path, os.R_OK):
                self.console.log(
                    f":magnifying_glass_tilted_left: Reading prompt from {prompt_path}"
                )

                self.prompt_path = prompt_path
            else:
                raise Exception(f"Cannot access prompt file {prompt_path}")
        else:
            self.create_default_config(prompt_path)

    def start(self):
        self.prepare_prompt_path()

        # a vital hack to pass the prompt path to the web ui
        os.environ["__PRR_WEB_UI_PROMPT_PATH"] = self.prompt_path

        uvicorn.run(
            "prr.ui:app", host="localhost", port=8400, reload=False, access_log=False
        )
