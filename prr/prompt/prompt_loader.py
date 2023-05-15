from . import Prompt

class PromptLoader:
  def __init__(self):
    self.dependency_files = []
    self.prompt = None
  
  def load_from_path(path):
    if is_file_yaml(path):
      self.__load_yaml_file(path)
    else:
      self.__load_text_file(path)

    return Prompt(path)

  def load_from_string(content):
    return Prompt(path)

  #####################################

  def __is_file_yaml(path):
    root, extension = os.path.splitext(path)

    if extension == ".yaml":
        return True

    return False


  def __load_text_file(self, path):
    self.path = path

    with open(path, "r") as stream:
      file_contents = self.deal_with_shebang_line(stream)
      self.template = self.template_env.from_string(file_contents)

  def __load_yaml_file(self, path):
    with open(path, "r") as stream:
      try:
          file_contents = self.deal_with_shebang_line(stream)
          data = yaml.safe_load(file_contents)
          self.path = path
      except yaml.YAMLError as exc:
          print(exc)

      if data:
          if data["services"]:
              self.parse_services(data["services"])
          if data["prompt"]:
              self.parse_prompt_config(data["prompt"])
