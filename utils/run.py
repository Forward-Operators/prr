#!/usr/bin/env python3.10

import sys

sys.path.append('.')
sys.path.append('/opt/conda/lib/python3.10/site-packages')

from dotenv import load_dotenv
load_dotenv()

from lib.prompt.library import Library
from lib.runner import Runner

library = Library("prompts")
prompt = library.get("concept-maps/subconcepts-of-buddhism.txt")

model = "openai/gpt-3.5-turbo"
# model = "anthropic/claude-v1"

runner = Runner(prompt, model)
runner.run()

result = runner.get_result()
stats = runner.get_stats()