def default_config_from_model_provider_name(model_provider_name):
  provider_name, model_name = model_provider_name.split("/")

  return {
    'model': model_provider_name,
    'provider_name': provider_name,
    'model_name': model_name
  }


class PromptConfig:
  def __init__(self, config_dictionary):
    """Initialize the PromptConfig class with a specified configuration dictionary ready from config file."""
    self.config = config_dictionary

  def __str__(self):
    return str(self.config)

  def models(self):
    """Get the list of models from the configuration file.
    
    Returns:
        list: The list of strings with model names in provider_name/model_name format or configuration names.
    """
    _models = self.config.get('models', [])

    if isinstance(_models, list):
      return _models
    elif isinstance(_models, dict):
      if 'models' in _models:
        return _models['models']
      else:
        return list(filter(lambda key: key != 'all', _models.keys()))

  def model(self, model_config_name):
    """Get the configuration for a specific model.
    
    Args:
        model_name (str): The name of the model in the configuration file - either configuration name or provider_name/provider_model format.
        
    Returns:
        dict: The model configuration as a dictionary.
    """

    models_config = self.config.get('models', {})

    if isinstance(models_config, list):
      # if we just have models listed there's no config at all
      #  models:
      #    - 'openai/gpt-3.5-turbo'
      #    - 'anthropic/claude-v1'
      return default_config_from_model_provider_name(model_config_name)
    
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

        # get defaults for all models listed
        all_models_config = models_config.copy()
        all_models_config.pop('models')

        # default model config
        model_config = default_config_from_model_provider_name(model_config_name)

        # update with defaults
        model_config.update(all_models_config)

        return model_config
      
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

        # get all section as default
        all_models_config = models_config.get('all', {})

        original_model_config = models_config.get(model_config_name, {})
        model_provider_name = original_model_config['model']

        model_config = default_config_from_model_provider_name(model_provider_name)

        # overload it with model-specific config
        model_config.update(original_model_config)
        model_config.update({'model_config_name': model_config_name})

        return model_config


    raise "Invalid models configuration."

  def get_expect_config(self):
    """Get the 'expect' configuration.
    
    Returns:
        dict: The 'expect' configuration as a dictionary.
    """
    return self.config.get('expect', {})
    