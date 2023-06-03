import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")))

from prr.prompt.model_options import ModelOptions
from prr.prompt.prompt_config import PromptConfig

from prr.services.providers.elevenlabs.tts import ServiceElevenLabsTTS

class TestElevenLabsTTS:
    def test_render_basic_prompt(self):
        config = PromptConfig()
        config.load_from_config_contents(
            """
prompt:
  content: 'foo bar'
services:
  eleven:
    model: 'elevenlabs/tts/eleven_multilingual_v1'
"""
        )

        assert config is not None

        service_config = config.service_with_name('eleven')

        service = ServiceElevenLabsTTS(
          config, 
          None, 
          service_config)

        assert service is not None

        rendered_prompt = service.render_prompt()

        assert rendered_prompt == 'foo bar'
