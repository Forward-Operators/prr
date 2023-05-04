import sys

from .prompt_run import PromptRun

# high-level class to run prompts based on configuration
class Runner:
  def __init__(self, prompt, config):
    self.prompt = prompt
    self.config = config

  # runs all models defined for specified prompt
  def run_all_configured_models(self):
    configured_models = self.config.models()

    results = {}

    for model in configured_models:
      model_config = self.config.model(model)
      results[model] = PromptRun(self.prompt, model_config).run()

    return results