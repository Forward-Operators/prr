import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from prr.prompt.prompt_config import PromptConfig
from prr.options import ModelOptions

class TestPromptConfig:

  def test_basic_parsing(self):
    config = PromptConfig()
    config.load_from_config_contents("""
prompt:
  content: 'foo bar'
""")

    assert config.template.render_text() == 'foo bar'
    assert config.template.render_messages() == [
      {
        'content': 'foo bar',
        'role': 'user'
      }
    ]

  def test_basic_services_model_list(self):
    config = PromptConfig()
    config.load_from_config_contents("""
prompt:
  content: 'foo bar'
services:
  models:
    - 'openai/chat/gpt-4'
    - 'anthropic/complete/claude-v1.3'
  options:
    temperature: 0.42
    max_tokens: 1337
""")

    assert config is not None
    services = config.configured_services()

    assert services == ['openai/chat/gpt-4', 'anthropic/complete/claude-v1.3']
    
    for service_name in services:
      assert config.option_for_service(service_name, 'temperature') == 0.42
      assert config.option_for_service(service_name, 'max_tokens') == 1337

  def test_basic_services_model_list_no_options(self):
    config = PromptConfig()
    config.load_from_config_contents("""
prompt:
  content: 'foo bar'
services:
  models:
    - 'openai/chat/gpt-4'
    - 'anthropic/complete/claude-v1.3'
""")

    assert config is not None
    services = config.configured_services()

    assert services == ['openai/chat/gpt-4', 'anthropic/complete/claude-v1.3']
    
    for service_name in services:
      assert config.option_for_service(service_name, 'temperature') == ModelOptions.DEFAULT_OPTIONS['temperature']
      assert config.option_for_service(service_name, 'max_tokens') == ModelOptions.DEFAULT_OPTIONS['max_tokens']
      assert config.option_for_service(service_name, 'top_k') == ModelOptions.DEFAULT_OPTIONS['top_k']
      assert config.option_for_service(service_name, 'top_p') == ModelOptions.DEFAULT_OPTIONS['top_p']

  def test_services(self):
    config = PromptConfig()
    config.load_from_config_contents("""
prompt:
  content: 'foo bar'
services:
  gpt4:
    model: 'openai/chat/gpt-4'
    options:
      max_tokens: 2048
  claude13:
    model: 'anthropic/complete/claude-v1.3'
    options:
      temperature: 0.84
  claude_default:
    model: 'anthropic/complete/claude-v1'
  options:
    temperature: 0.42
    max_tokens: 1337
""")

    assert config is not None
    services = config.configured_services()

    assert services == ['gpt4', 'claude13', 'claude_default']
    
    assert config.option_for_service('gpt4', 'temperature') == 0.42
    assert config.option_for_service('gpt4', 'max_tokens') == 2048

    assert config.option_for_service('claude13', 'temperature') == 0.84
    assert config.option_for_service('claude13', 'max_tokens') == 1337

    assert config.option_for_service('claude_default', 'temperature') == 0.42
    assert config.option_for_service('claude_default', 'max_tokens') == 1337
