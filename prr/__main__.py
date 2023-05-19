#!/usr/bin/env python

import argparse
import os
import sys

from prr.commands.run import RunPromptCommand
from prr.commands.watch import WatchPromptCommand
from prr.prompt.model_options import ModelOptions
from prr.utils.config import load_config

config = load_config()


def main():
    parser = argparse.ArgumentParser(
        description="Run a prompt against configured models.",
        prog="prr",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    sub_parsers = parser.add_subparsers(help="command to execute", dest="command")

    run_parser = sub_parsers.add_parser(
        "run", help="run prompt against models (default option)"
    )
    watch_parser = sub_parsers.add_parser(
        "watch", help="watch prompts/config changes to launch re-runs"
    )
    script_parser = sub_parsers.add_parser(
        "script", help="prompt script mode for use with #!/usr/bin/prr"
    )

    def add_common_args(_parser):
        _parser.add_argument(
            "--abbrev",
            help="Abbreviate prompts and completions",
            action="store_true",
            default=False,
        )

        _parser.add_argument(
            "--service",
            "-s",
            help="Service to use if none is configured (defaults to DEFAULT_SERVICE)",
            default=config.get("DEFAULT_SERVICE"),
            type=str,
        )

        _parser.add_argument(
            "--temperature",
            "-t",
            help="Temperature (defaults to DEFAULT_TEMPERATURE)",
            type=float,
        )

        _parser.add_argument(
            "--max_tokens",
            "-mt",
            help="Max tokens to use (defaults to DEFAULT_MAX_TOKENS)",
            type=int,
        )

        _parser.add_argument(
            "--top_p",
            "-tp",
            help="Sets a cumulative probability threshold for selecting candidate tokens, where only tokens with a cumulative probability higher than the threshold are considered, allowing for flexible control over the diversity of the generated output (defaults to DEFAULT_TOP_P).",
            type=int,
        )

        _parser.add_argument(
            "--top_k",
            "-tk",
            help="Determines the number of top-scoring candidate tokens to consider at each decoding step, effectively limiting the diversity of the generated output (defaults to DEFAULT_TOP_K)",
            type=int,
        )

        _parser.add_argument(
            "--quiet",
            "-q",
            help="Quiet mode, just outputs the completion",
            action="store_true",
            default=False,
        )
        _parser.add_argument(
            "--log",
            "-l",
            help="Save each run in <prompt>.runs directory",
            action="store_true",
            default=False,
        )
        _parser.add_argument("prompt_path", help="Path to prompt to run")

    add_common_args(run_parser)
    add_common_args(watch_parser)
    add_common_args(script_parser)

    watch_parser.add_argument(
        "--cooldown", "-c", type=int, help="How much to wait after a re-run", default=5
    )

    args, prompt_args = parser.parse_known_args()
    parsed_args = vars(args)

    if parsed_args["command"] == "script":
        parsed_args["quiet"] = True
        parsed_args["abbrev"] = False
        command = RunPromptCommand(parsed_args, prompt_args)
        command.run_prompt()

    if parsed_args["command"] == "run":
        command = RunPromptCommand(parsed_args)
        command.run_prompt()

    if parsed_args["command"] == "watch":
        command = WatchPromptCommand(parsed_args)
        command.watch_prompt()


if __name__ == "__main__":
    main()
