import os

import jinja2
import yaml
from jinja2 import meta

from prr.prompt.prompt_config import PromptConfig
from prr.prompt.prompt_template import PromptTemplate
from prr.prompt.service_config import ServiceConfig


class Prompt:
    def __init__(self, content, config=None, args=None):
        self.content = content
        self.config = config
        self.args = args
