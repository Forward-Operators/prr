#!/usr/bin/env python3.10

import sys
sys.path.append('.')
# sys.path.append('/home/codespace/.local/lib/python3.10/site-packages')
sys.path.append('/opt/conda/lib/python3.10/site-packages')

from dotenv import load_dotenv
load_dotenv()

from colored import fg, bg, attr

from lib.prompt.library import Library
from lib.runner import Runner

library = Library("prompts")
prompt = library.get("concept-maps/subconcepts-of-buddhism.txt")

runner = Runner(prompt, "openai/gpt-3.5-turbo")
# runner = Runner(prompt, "anthropic/claude-v1")

runner.run()

result = runner.get_result()
stats = runner.get_stats()

# print ("=====================")

# print (fg("green"))
# print (result)
# print (fg("red"))
# print (stats)