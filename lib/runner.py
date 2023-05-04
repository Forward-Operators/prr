import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

from .prompt.prompt import Prompt
from .llms.providers.openai import LLMProviderOpenAI
from .llms.providers.anthropic import LLMProviderAnthropic
from .llms.stats import PromptRunStats
from .llms.response import ModelResponse

from colored import fg, attr

# takes prompt and model, finds provider, runs the prompt
class PromptRun:
  def __init__(self, prompt, model):
    self.prompt = prompt
    self.provider_name, self.model_name = model.split("/")
    self.model = self.model_name

    if self.provider_name == "openai":
      self.provider = LLMProviderOpenAI()
    elif self.provider_name == "anthropic":
      self.provider = LLMProviderAnthropic()
    else:
      raise Exception("Unknown provider: " + self.provider_name)

    self.stats = PromptRunStats(prompt, model)
    self.response = ModelResponse()

  def prompt_template_len(self):
    return len(self.prompt.template)

  def prompt_abbrev(self):
    if self.prompt_template_len() > 40:
      return self.prompt.template[0:40] + "..."
    else:
      return self.prompt.template

  def response_completion_len(self):
    return self.response.completion_len()

  def response_abbrev(self):
    return self.response.completion_abbrev()

  def model_id(self):
    return "/".join([self.provider_name, self.model_name])
  
  def describe_options(self, options):
    parts = []

    if options:
      if options['temperature']:
        parts.append(f"temp={options['temperature']}")

      if options['max_tokens']:
        parts.append(f"max_tokens={options['max_tokens']}")

    return " ".join(parts)

  def run(self, options):
    if options.get('config_name'):
      model_description = options['config_name'] + " (" + self.model_id() + ")"
    else:
      model_description = self.model_id()

    eprint ('🧠 {model_description}: {options_description} prompt_size={template_bytes}'.format(
      model_description=model_description,
      template_bytes=self.prompt_template_len(),
      options_description=self.describe_options(options)))
    
    self.stats.before_run()
    self.response = ModelResponse(self.provider.run(self.prompt, self.model, options))
    self.stats.after_run()

    _stats = self.stats.get_stats()
    elapsed_time = round(_stats['elapsed_time'], 2)

    eprint ('✅ {model_description}: received {response_bytes} bytes in {response_elapsed_time}s'.format(
      model_description=model_description,
      response_elapsed_time=elapsed_time,
      response_bytes=self.response_completion_len()))

  def get_stats(self):
    return self.stats.get_stats()
  
  def get_result(self):
    return self.response
  

class Runner:
  def __init__(self, prompt):
    self.prompt = prompt

  def run_all_configured_models(self, option_overrides={}):
    # print ("\n\n\n")
    # print ("-*- run_all_configured_models -*-")

    models_defined = self.prompt.config.models()

    # print ('models: ', models_defined)

    results = {}

    for model in models_defined:
      model_config = self.prompt.config.model(model)
      # print ('\n')
      # print (f'----- running model [{model}] -----')
      # print (model_config)
      # print ('\n')

      results[model] = {
        'config': model_config        
      }

      prompt_run = PromptRun(self.prompt, model_config['model'])
      prompt_run.run(model_config)

      results[model]['results'] = prompt_run.get_result()
      results[model]['stats'] = prompt_run.get_stats()

    return results