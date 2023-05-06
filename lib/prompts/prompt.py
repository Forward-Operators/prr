import os
import yaml
import jinja2

class Prompt:
  def __init__(self, path):
    self.messages = None
    self.template = None
    self.dependency_files = []

    root, extension = os.path.splitext(path)

    if extension == ".yaml":
      self.load_yaml_file(path)
    else:
      self.load_text_file(path)

  def parse_messages(self, messages):
    # expand content_file field in messages
    self.messages = []
    self.dependency_files = []
    root_path = os.path.dirname(self.path)

    if messages:
      for message in messages:
        if message.get('content_file'):
          updated_message = message.copy()
          file_path = os.path.join(root_path, updated_message.pop("content_file"))
          
          with open(file_path, "r") as f:
            updated_message.update({"content": f.read()})
            self.messages.append(updated_message)
            self.dependency_files.append(file_path)
        else:
          self.messages.append(message)


  def load_yaml_file(self, path):
    with open(path, "r") as stream:
      try:
        data = yaml.safe_load(stream)
        self.path = path
      except yaml.YAMLError as exc:
        print(exc)

      self.parse_messages(data['messages'])

  def load_text_file(self, path):
    with open(path, "r") as f:
      raw_text = f.read()
      template_loader = jinja2.FileSystemLoader(searchpath=os.path.dirname(path))
      template_env = jinja2.Environment(loader=template_loader)
      self.template = template_env.get_template(os.path.basename(path))

      # self.template = template.render(name='John Doe')
      
      self.path = path

  def message_text_description(self, message):
    name = message.get('name')
    role = message.get('role')
    content = message.get('content')

    if name:
      return f'{name} ({role}): {content}'
    else:
      return f'{role}: {content}'

  def text(self):
    if self.messages:
      return "\n".join([self.message_text_description(msg) for msg in self.messages])
    
    return self.template.render()
  
  def text_len(self):
    return len(self.text())
  
  def dump(self):
    return yaml.dump({
      "text": self.text,
      "messages": self.messages
    })
  
  def text_abbrev(self, max_len = 25):
    if self.text_len() > max_len:
      str = self.text()[0:max_len] + "..."
    else:
      str = self.text()

    return str.replace("\n", " ").replace("  ", " ")