#!/usr/bin/env python3

import sys
sys.path.append('/opt/conda/lib/python3.10/site-packages')
sys.path.append('.')

from dotenv import load_dotenv
load_dotenv()

from colored import fg, bg, attr

from lib.runner import Runner
from lib.prompt.library import Library

library = Library("prompts")
prompt = library.get("common/highest-peak")

runner = Runner(prompt, "openai/gpt-3.5-turbo")

result = runner.run()

print (fg("green") + result)