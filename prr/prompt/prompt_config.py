import yaml

from ..service_config import ServiceConfig
from .prompt_template import PromptTemplateSimple, PromptTemplateMessages

class PromptConfig:
  # raw_config_content is text to be parsed into YAML
  def __init__(self, raw_config_content, search_path='.'):
    # where are we supposed to look for referenced files
    self.search_path = search_path

    # raw YAML string
    self.raw_config_content = raw_config_content

    # prompt: (PromptTemplate)
    self.prompt = None

    # services: (ServiceConfig)
    self.services = {}

    # version: 1
    self.version = None

    # parse raw YAML content into a dictionary
    self.__parse_raw()

    # parse that dictionary into respective parts of prompt config
    self.__parse()

  # list keys/names of all services that we have configured in the config file
  def configured_services(self):
    return list(self.services.keys())

  # returns options for specific service, already includes all option inheritance
  # def options_for_service(self, service_name):
  #   return self.services[service_name]

  def option_for_service(self, service_name, option_name):
    return self.services[service_name].options.option(option_name)

  ####################################################

  def __parse(self):
    self.__parse_version()
    self.__parse_prompt()
    self.__parse_services()

  def __parse_raw(self):
    try:
      self.config_content = yaml.safe_load(self.raw_config_content)
    except yaml.YAMLError as exc:
      print(exc)

  def __parse_version(self):
    if self.config_content:
      self.version = self.config_content.get('version')

  # high level "prompt:" parsing
  def __parse_prompt(self):
    if self.config_content:
      prompt = self.config_content.get('prompt')

      if prompt:
        content_file = prompt.get('content_file')
        content = prompt.get('content')
        messages = prompt.get('messages')

        if content_file:
          with open(content_file, "r") as file:
            file_contents = file.read()
            self.prompt = PromptTemplateSimple(file_contents, self.search_path)
        elif content:
          self.prompt = PromptTemplateSimple(content, self.search_path)
        elif messages:
          self.prompt = PromptTemplateMessages(messages, self.search_path)

  # high level "services:" parsing
  def __parse_services(self):
    if self.config_content:
      _services = self.config_content.get('services')

      if _services:
        options_for_all_services = _services.get('options')

        # 
        # if we have models + prompt-level model options
        # 
        # services:
        #   models:
        #     - 'openai/chat/gpt-4'
        #     - 'anthropic/complete/claude-v1.3-100k'
        #   options:
        #     max_tokens: 1337
        _models = _services.get('models')
        if _models:
          for _model_name in _models:
            service_config = ServiceConfig(_model_name,
                                           _model_name, 
                                           options_for_all_services)

            self.services[_model_name] = service_config

        else:
          # 
          # if we have services defined with options for each
          # 
          # services:
          #   mygpt4:
          #     model: 'openai/chat/gpt-4'
          #     options:
          #       temperature: 0.2
          #       max_tokens: 4000
          #   options:
          #     max_tokens: 1337
          for _service_name in _services:
            if _service_name not in ['options', 'models']:
              service = _services[_service_name]

              # start with options for all services
              # defined on a higher level
              options = options_for_all_services.copy()

              # update with service-level options
              service_level_options = service.get('options')

              if service_level_options:
                options.update(service_level_options)

              model = service.get('model')

              service_config = ServiceConfig(_service_name, model, options)

              self.services[_service_name] = service_config
