from . import Prompt

class PromptLoader:
  def __init__(self):
    dependency_files = []
    # 
  
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


  def __load_text_file(self, path):
    self.path = path

    with open(path, "r") as stream:
      file_contents = self.deal_with_shebang_line(stream)
      self.template = self.template_env.from_string(file_contents)
