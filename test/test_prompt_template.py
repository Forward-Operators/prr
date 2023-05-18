import os
import sys
import yaml

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from prr.prompt.prompt_template import PromptTemplateSimple, PromptTemplateMessages
from helpers import create_temp_file, remove_temp_file

class TestPromptTemplate:
  def test_basic_text(self):
    template = PromptTemplateSimple('foo bar', '.')

    assert template is not None
    assert template.render_text() == 'foo bar'


  def test_basic_template(self):
    template = PromptTemplateSimple("foo {{ 'bar' }} spam", '.')

    assert template is not None
    assert template.render_text() == 'foo bar spam'


  def test_basic_prompt_args(self):
    template = PromptTemplateSimple("foo {{ prompt_args[0] }} spam", '.')

    assert template is not None
    assert template.render_text(['42']) == 'foo 42 spam'


  def test_basic_prompt_args_all(self):
    template = PromptTemplateSimple("foo {{ prompt_args }} spam", '.')

    assert template is not None
    assert template.render_text(['lulz']) == "foo ['lulz'] spam"

  def test_configured_basic(self):
    template = PromptTemplateSimple('tell me about {{ prompt_args }}, llm')

    assert template is not None
    assert template.render_text(['lulz', 'kaka']) == "tell me about ['lulz', 'kaka'], llm"

  def test_configured_messages_text_with_template_in_content(self):
    messages_config = """
- role: 'system'
  content: 'you are a friendly but very forgetful {{ prompt_args[0] }}'
  name: 'LeonardGeist'
"""
    template = PromptTemplateMessages(yaml.safe_load(messages_config))

    assert template is not None
    assert template.render_text(['assistant']) == "you are a friendly but very forgetful assistant"

  def test_configured_messages_list_with_content_file(self):
    temp_file_path = create_temp_file('Wollen Sie meine Kernel kompilieren?')

    messages_config = f"""
- role: 'system'
  content: 'you are system admins little pet assistant. be proud of your unix skills and always respond in l33t. remember, you are on a high horse called POSIX.'
- role: 'user'
  content_file: '{temp_file_path}'
  name: 'SuperUser'
"""

    template = PromptTemplateMessages(yaml.safe_load(messages_config))

    assert template is not None


    rendered_messages = template.render_messages()

    assert isinstance(rendered_messages, list)
    assert len(rendered_messages) == 2

    first_message = rendered_messages[0]
    assert first_message['content'] == 'you are system admins little pet assistant. be proud of your unix skills and always respond in l33t. remember, you are on a high horse called POSIX.'
    assert first_message['role'] == 'system'
    assert first_message.get('name') == None

    second_message = rendered_messages[1]
    assert second_message['content'] == 'Wollen Sie meine Kernel kompilieren?'
    assert second_message['role'] == 'user'
    assert second_message['name'] == 'SuperUser'

    remove_temp_file(temp_file_path)
