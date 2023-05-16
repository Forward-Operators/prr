import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from prr.prompt.prompt_config import PromptConfig

class TestPromptConfig:

  def test_basic_parsing(self):
    config = PromptConfig("""
prompt:
  content: 'foo bar'
""")

    assert config is not None
    assert config.config_content['prompt']['content'] == 'foo bar'
