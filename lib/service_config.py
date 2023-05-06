from .options import ModelOptions

class ServiceConfig():
  def __init__(self, model, options = None):
    self.model = model
    self.options = ModelOptions(options or {})

  def model_name(self):
    return self.model.split('/')[-1]

  def service_key(self):
    return '/'.join(self.model.split('/')[:-1])