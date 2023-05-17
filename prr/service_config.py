from .options import ModelOptions

class ServiceConfig:
  def __init__(self, name, model, options=None):
    self.name = name   # service name, e.g. "mygpt5"
    self.model = model # model name, e.g. "openai/chat/gpt-5"        
    self.options = ModelOptions(options or {})

    # def config_name(self):
    #     return self.model

    # def model_name(self):
    #     return self.model.split("/")[-1]

    # def service_key(self):
    #     return "/".join(self.model.split("/")[:-1])

  def to_dict(self):
    return {
      "model": self.config_name(), 
      "options": self.options.to_dict()
    }
