#!/usr/bin/env python3.10

DEFAULT_MODEL = "openai/gpt-3.5-turbo"

import sys
sys.path.append('.')
sys.path.append('/opt/conda/lib/python3.10/site-packages')

import argparse

from dotenv import load_dotenv
load_dotenv()

from lib.prompt.library import Library
from lib.runner import Runner

parser = argparse.ArgumentParser(description="Run a prompt against a model.",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-m", "--model", help="model to use", default=DEFAULT_MODEL)
parser.add_argument("-mt", "--max_tokens", help="max tokens to use", default=128)
parser.add_argument("-t", "--temperature", help="temperature", default=1)
parser.add_argument("-tk", "--top_k", help="top_k")
parser.add_argument("-tp", "--top_p", help="top_p")
# parser.add_argument("-v", "--verbose", action="store_true", help="increase verbosity")
parser.add_argument("prompt_path", help="Path to prompt to run")
args = parser.parse_args()
config = vars(args)

library = Library("prompts")
prompt = library.get_prompt(config["prompt_path"])

model = config["model"] or DEFAULT_MODEL
# model = "anthropic/claude-v1"

runner = Runner(prompt, model)

runner.run({
  "max_tokens": int(config["max_tokens"]),
  "temperature": float(config["temperature"]),
  "top_k": config["top_k"],
  "top_p": config["top_p"]
})

result = runner.get_result()
stats = runner.get_stats()

print(result.completion)