import yaml

class PromptConfig:
  def __init__(self, raw_config_content):
    self.raw_config_content = raw_config_content

    self.__parse_raw_config()


  def __parse_raw_config(self):
    try:
      self.config_content = yaml.safe_load(self.raw_config_content)
    except yaml.YAMLError as exc:
      print(exc)
