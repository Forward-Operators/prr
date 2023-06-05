import os
import sys

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
)

from prr.prompt.model_options import ModelOptions
from prr.prompt.prompt_config import PromptConfig
from prr.services.providers.openai.chat import ServiceOpenAIChat


class TestOpenAIChat:
    def test_render_basic_prompt(self):
        config = PromptConfig()
        config.load_from_config_contents(
            """
prompt:
  content: 'spam eggz'
services:
  gpt4:
    model: 'openai/chat/gpt-4'
"""
        )

        assert config is not None

        service_config = config.service_with_name("gpt4")

        service = ServiceOpenAIChat(config, None, service_config)

        assert service is not None

        rendered_prompt = service.render_prompt()

        assert rendered_prompt == [{"content": "spam eggz", "role": "user"}]

    def test_render_longer_prompt(self):
        config = PromptConfig()
        config.load_from_config_contents(
            """
prompt:
  messages:
    - role: 'system'
      content: 'You, GPT, are a little Chihuahua dog. That is all you need to know.'
    - role: 'user'
      content: 'Also, you walk like a duck.'
    - role: 'assistant'
      content: 'What the hell is goin on?'
      name: 'GPT'
    - role: 'user'
      content: 'Bark, bark, bark!'
services:
  gpt35:
    model: 'openai/chat/gpt-3.5-turbo'
"""
        )

        assert config is not None

        service_config = config.service_with_name("gpt35")

        service = ServiceOpenAIChat(config, None, service_config)

        assert service is not None

        rendered_prompt = service.render_prompt()

        print(rendered_prompt)

        assert rendered_prompt == [
            {
                "role": "system",
                "content": "You, GPT, are a little Chihuahua dog. That is all you need to know.",
            },
            {"role": "user", "content": "Also, you walk like a duck."},
            {
                "role": "assistant",
                "content": "What the hell is goin on?",
                "name": "GPT",
            },
            {"role": "user", "content": "Bark, bark, bark!"},
        ]
