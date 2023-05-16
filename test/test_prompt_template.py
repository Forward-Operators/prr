import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from prr.prompt.prompt_template import PromptTemplate

class TestPromptTemplate:

  def test_basic_text(self):
    template = PromptTemplate('foo bar', '.')

    assert template is not None
    assert template.text() == 'foo bar'


  def test_basic_template(self):
    template = PromptTemplate("foo {{ 'bar' }} spam", '.')

    assert template is not None
    assert template.text() == 'foo bar spam'

  def test_basic_prompt_args(self):
    template = PromptTemplate("foo {{ prompt_args[0] }} spam", '.')

    assert template is not None
    assert template.text(['42']) == 'foo 42 spam'