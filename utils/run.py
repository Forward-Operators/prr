#!/usr/bin/env python3

import sys

sys.path.append('/opt/conda/lib/python3.10/site-packages')

from dotenv import load_dotenv

load_dotenv()

import openai

# openai.api_key = "sk-..."

# list models
models = openai.Model.list()

# print the first model's id
print(models.data[0].id)

# create a completion
completion = openai.Completion.create(model="ada", prompt="Hello world")

# print the completion
print(completion.choices[0].text)
