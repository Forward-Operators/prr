import jinja2

class PromptMessage:
  def __init__(self, content_template_string, search_path='.', role='user', name=None):
    self.content_template_string = content_template_string
    self.search_path = search_path
    self.role = role
    self.name = name

    template_loader = jinja2.FileSystemLoader(searchpath=self.search_path)
    template_env = jinja2.Environment(loader=template_loader)
    self.template = template_env.from_string(self.content_template_string)

  def render_text(self, args=[]):
    return self.template.render({"prompt_args": args})

  def render_message(self, args=[]):
    _message = {
      'role': self.role,
      'content': self.render_text(args)
    }

    if self.name:
      _message.update({ 'name': self.name })

    return _message

# base class
class PromptTemplate:
  def __init__(self):
    self.messages = []

  def render_text(self, args=[]):
    rendered_texts = [message.render_text(args) for message in self.messages]

    return "\n".join(rendered_texts)

  def render_messages(self, args=[]):
    return [message.render_message(args) for message in self.messages]

# just a text/template file or prompt.contents from config
class PromptTemplateSimple(PromptTemplate):
  def __init__(self, template_string, search_path='.'):
    self.messages = [
      PromptMessage(template_string, search_path, 'user')
    ]

# prompt.messages: key from config
class PromptTemplateMessages(PromptTemplate):
  # 'messages' are passed here verbatim after parsing YAML
  def __init__(self, messages, search_path='.'):
    super().__init__()

    for message in messages:
      prompt_message = None

      role = message.get('role')
      name = message.get('name')
      content = message.get('content')
      content_file = message.get('content_file')

      if content:
        prompt_message = PromptMessage(content, search_path, role, name)
      elif content_file:
        include_contents = "{% include '" + content_file + "' %}"
        prompt_message = PromptMessage(include_contents, search_path, role, name)

      if prompt_message:
        self.messages.append(prompt_message)
