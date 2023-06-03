import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")))

from prr.prompt.model_options import ModelOptions
from prr.prompt.prompt_config import PromptConfig

from prr.services.providers.google.chat import ServiceGoogleChat

class TestGoogleChat:
    def test_render_basic_prompt(self):
        config = PromptConfig()
        config.load_from_config_contents(
            """
prompt:
  content: 'foo bar'
services:
  sergey:
    model: 'google/chat/chat-bison'
  options:
    temperature: 0.71
    max_tokens: 420
"""
        )

        assert config is not None

        service_config = config.service_with_name('sergey')

        service = ServiceGoogleChat(
          config, 
          None, 
          service_config)

        assert service is not None

        rendered_prompt = service.render_prompt()

        assert rendered_prompt == {
          'context': '', 
          'messages': [
            {
              'author': 'user', 
              'content': 'foo bar'
            }
          ]
        }


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
  bison:
    model: 'google/chat/chat-bison'
"""
        )

        assert config is not None

        service_config = config.service_with_name('bison')

        service = ServiceGoogleChat(
          config, 
          None, 
          service_config)

        assert service is not None

        rendered_prompt = service.render_prompt()

        assert rendered_prompt == {
          'context': 'You, Claude, are a little Chihuahua dog. That is all you need to know.', 
          'messages': [
            {
              'author': 'user', 
              'content': 'Also, you walk like a duck.'
            }, 
            {
              'author': 'bot', 
              'content': 'What the hell is goin on?'
            }, 
            {
              'author': 'user', 
              'content': 'Bark, bark, bark!'
            }
          ]
        }

