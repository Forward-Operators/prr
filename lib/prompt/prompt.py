class PromptConfig:
  def __init__(self, config_dictionary):
    """Initialize the PromptConfig class with a specified configuration dictionary ready from config file."""
    self.config = config_dictionary

  def models(self):
    """Get the list of models from the configuration file.
    
    Returns:
        list: The list of models.
    """
    _models = self.config.get('models', [])

    if isinstance(_models, list):
      return _models
    elif isinstance(_models, dict):
      if 'models' in _models:
        return _models['models']
      else:
        return list(filter(lambda key: key != 'all', _models.keys()))

  def model(self, model_name):
    """Get the configuration for a specific model.
    
    Args:
        model_name (str): The name of the model in the configuration file.
        
    Returns:
        dict: The model configuration as a dictionary.
    """

    models_config = self.config.get('models', {})

    if isinstance(models_config, list):
      # if we just have models listed there's no config at all
      #  models:
      #    - 'openai/gpt-3.5-turbo'
      #    - 'anthropic/claude-v1'
      return { 'model': model_name }
    elif isinstance(models_config, dict):
      model_names = models_config.get('models', {})
      if model_names:
        # we have a config for each model or one general config
        #  models:
        #    models: 
        #      - 'openai/gpt-3.5-turbo'
        #      - 'anthropic/claude-v1'
        #    temperature: 0.7
        #    max_tokens: 100
        #
        general_config = models_config.copy()

        # remove the models key
        general_config.pop('models')

        return general_config
      
      else:
        # we have a config for each model and maybe
        # a general config for all models in "all" key

        # models:
        #   gpt4crazy:
        #     model: 'openai/gpt-4'
        #     temperature: 0.99
        #   claudev1smart:
        #     model: 'anthropic/claude-v1'
        #     temperature: 0
        #   all:
        #     temperature: 0.7
        #     max_tokens: 64

        general_config = models_config.get('all', {})

        model_config = models_config.get(model_name, {})

        # not let's override "all" config with specific per-model settings
        merged_config = general_config.copy()

        # now let's override values from 'all' with specific model options
        merged_config.update(model_config)

        return merged_config


    raise "Invalid models configuration."

  def get_expect_config(self):
    """Get the 'expect' configuration.
    
    Returns:
        dict: The 'expect' configuration as a dictionary.
    """
    return self.config.get('expect', {})
    
class Prompt:
  def __init__(self, template, config_dictionary):
    self.template = template
    self.config = PromptConfig(config_dictionary)

  def text(self, model="openai/gpt-4"):
    return self.template