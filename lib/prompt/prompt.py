class PromptConfig:
  def __init__(self, config_dictionary):
    """Initialize the PromptConfig class with a specified configuration dictionary ready from config file."""
    self.config = config_dictionary

  def get_model_config(self, model_name):
    """Get the configuration for a specific model.
    
    Args:
        model_name (str): The name of the model in the configuration file.
        
    Returns:
        dict: The model configuration as a dictionary.
    """
    return self.config.get('models', {}).get(model_name, {})

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