import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")))

from prr.prompt.model_options import ModelOptions
from prr.prompt.prompt_config import PromptConfig

from prr.services.providers.google.complete import ServiceGoogleComplete

class TestGoogleComplete:
    def test_render_basic_prompt(self):
        config = PromptConfig()
        config.load_from_config_contents(
            """
prompt:
  content: 'To be, or not to be, that is the'
services:
  larry:
    model: 'google/complete/text-bison@001'
"""
        )

        assert config is not None

        service_config = config.service_with_name('larry')

        service = ServiceGoogleComplete(
          config, 
          None, 
          service_config)

        assert service is not None

        rendered_prompt = service.render_prompt()

        assert rendered_prompt == "To be, or not to be, that is the"

