import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")))

from prr.prompt.model_options import ModelOptions
from prr.prompt.prompt_config import PromptConfig

from prr.services.providers.bigcode.starcoder import ServiceBigcodeStarcoder

class TestBigcodeStarcoder:
    def test_render_basic_prompt(self):
        config = PromptConfig()
        config.load_from_config_contents(
            """
prompt:
  content: 'function hello_world() {'
services:
  starcoder:
    model: 'bigcode/starcoder/starcoder'
  options:
    temperature: 0
"""
        )

        assert config is not None

        service_config = config.service_with_name('starcoder')

        service = ServiceBigcodeStarcoder(
          config, 
          None, 
          service_config)

        assert service is not None

        rendered_prompt = service.render_prompt()

        assert rendered_prompt == "function hello_world() {"


    def test_render_longer_prompt(self):
        config = PromptConfig()
        config.load_from_config_contents(
            """
prompt:
  messages:
    - role: 'system'
      content: 'Rename this function to CamelCase: '
    - role: 'user'
      content: 'function hello_world() {'
services:
  starcoder:
    model: 'bigcode/starcoder/starcoder'
"""
        )

        assert config is not None

        service_config = config.service_with_name('starcoder')

        service = ServiceBigcodeStarcoder(
          config, 
          None, 
          service_config)

        assert service is not None

        rendered_prompt = service.render_prompt()

        assert rendered_prompt == """Rename this function to CamelCase: 
function hello_world() {"""