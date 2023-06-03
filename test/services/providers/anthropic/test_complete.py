import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")))

from prr.prompt.model_options import ModelOptions
from prr.prompt.prompt_config import PromptConfig

from prr.services.providers.anthropic.complete import ServiceAnthropicComplete

class TestAnthropicComplete:
    def test_render_basic_prompt(self):
        config = PromptConfig()
        config.load_from_config_contents(
            """
prompt:
  content: 'foo bar'
services:
  claude:
    model: 'anthropic/complete/claude-v1.3'
  options:
    temperature: 0.71
    max_tokens: 420
"""
        )

        assert config is not None

        service_config = config.service_with_name('claude')

        service = ServiceAnthropicComplete(
          config, 
          None, 
          service_config)

        assert service is not None

        rendered_prompt = service.render_prompt()

        assert rendered_prompt == "\n\nHuman: foo bar\n\nAssistant:"


    def test_render_longer_prompt(self):
        config = PromptConfig()
        config.load_from_config_contents(
            """
prompt:
  messages:
    - role: 'system'
      content: 'You, Claude, are a little Chihuahua dog. That is all you need to know.'
    - role: 'user'
      content: 'Also, you walk like a duck.'
    - role: 'assistant'
      content: 'What the hell is goin on?'
    - role: 'user'
      content: 'Bark, bark, bark!'
services:
  claude:
    model: 'anthropic/complete/claude-v1.3'
  options:
    temperature: 0.71
    max_tokens: 420
"""
        )

        assert config is not None

        service_config = config.service_with_name('claude')

        service = ServiceAnthropicComplete(
          config, 
          None, 
          service_config)

        assert service is not None

        rendered_prompt = service.render_prompt()

        assert rendered_prompt == """

Human: You, Claude, are a little Chihuahua dog. That is all you need to know. Also, you walk like a duck.

Assistant: What the hell is goin on?

Human: Bark, bark, bark!

Assistant:"""


