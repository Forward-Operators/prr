from . import Prompt
from .prompt_template import PromptTemplate, PromptTemplateSimple, PromptTemplateMessages

class PromptLoader:
  def __init__(self):
    self.dependency_files = []
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
        self.template = PromptTemplateSimple(file_contents, __search_path())

    except FileNotFoundError:
      print("The specified file does not exist.")

    except PermissionError:
      print("You do not have permission to access the specified file.")

    except Exception as e:
      print("An error occurred while opening the file:", str(e))      

  def __load_yaml_file(self, path):
    with open(path, "r") as stream:
      try:
        self.path = path
        self.config = PromptConfig(stream.read(), self.__search_path())
      
      except yaml.YAMLError as exc:
        print(exc)

      except FileNotFoundError:
        print("The specified file does not exist.")

      except PermissionError:
        print("You do not have permission to access the specified file.")

      except Exception as e:
        print("An error occurred while opening the file:", str(e))


  # def __add_file_dependency(self, path):
  #   if not path in self.dependency_files:
  #     self.dependency_files.append(path)
