from ..prompts.prompt_run import PromptRun
from .saver import PromptRunSaver

from ..llms.options import ModelOptions

# high-level class to run prompts based on configuration
class Runner:
  def __init__(self, prompt, config):
    self.prompt = prompt
    self.config = config
    self.saver = PromptRunSaver()

  def model_options_for_model(self, model_config_name):
    return ModelOptions(self.config.model(model_config_name))

  def run_model(self, model_config_name, save_run=False):
    model_config = self.config.model(model_config_name)

    result = PromptRun(self.prompt, model_config).run()

    if save_run:
      run_save_directory = self.saver.save(model_config_name, result)
    else:
      run_save_directory = None

    return result, run_save_directory

  def configured_models(self):
    if self.config:
      return self.config.models()

    return []

  # runs all models defined for specified prompt
  def run_all_configured_models(self):
    results = {}

    for model in self.configured_models():
      results[model] = self.run_model(model)

    return results