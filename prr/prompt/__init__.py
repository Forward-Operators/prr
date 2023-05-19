import os

import jinja2
import yaml
from jinja2 import meta

from .service_config import ServiceConfig

from .prompt_config import PromptConfig
from .prompt_template import PromptTemplate

class Prompt:
    def __init__(self, content, config=None, args=None):
        self.content = content
        self.config = config
        self.args = args

