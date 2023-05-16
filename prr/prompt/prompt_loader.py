from . import Prompt
from .prompt_template import PromptTemplate

class PromptLoader:
  def __init__(self):
    self.dependency_files = []
    self.template = None # PromptTemplate
    self.config = None   # PromptConfig
  
  def load_from_path(path):
    self.__add_file_dependency(path)

    if is_file_yaml(path):
      # prompt is in yaml config file format
      self.__load_yaml_file(path)
    else:
      # simple text (or jinja) file, no config
      self.__load_text_file(path)

    return Prompt(self.template, self.config)

  def load_from_string(content):
    return Prompt(content)

  #####################################

  def __is_file_yaml(path):
    root, extension = os.path.splitext(path)

    if extension == ".yaml":
        return True

    return False

  def __search_path():
    return os.path.dirname(self.path)

  def __load_text_file(self, path):
    self.path = path

    try:
      with open(path, "r") as file:
        file_contents = file.read()
        self.template = PromptTemplate(file_contents, __search_path())

    except FileNotFoundError:
      print("The specified file does not exist.")

    except PermissionError:
      print("You do not have permission to access the specified file.")

    except Exception as e:
      print("An error occurred while opening the file:", str(e))      


  def __load_yaml_file(self, path):
    with open(path, "r") as stream:
      try:
        file_contents = self.deal_with_shebang_line(stream)
        data = yaml.safe_load(file_contents)
        self.path = path
      except yaml.YAMLError as exc:
        print(exc)

      except FileNotFoundError:
        print("The specified file does not exist.")

      except PermissionError:
        print("You do not have permission to access the specified file.")

      except Exception as e:
        print("An error occurred while opening the file:", str(e))      

      if data:
          if data["services"]:
              self.parse_services(data["services"])
          if data["prompt"]:
              self.parse_prompt_config(data["prompt"])

  def __add_file_dependency(self, path):
    if not path in self.dependency_files:
      self.dependency_files.append(path)
