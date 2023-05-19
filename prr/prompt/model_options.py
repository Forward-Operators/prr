from prr.utils.config import load_config

ALLOWED_OPTIONS = ["max_tokens", "temperature", "top_k", "top_p"]


config = load_config()

class ModelOptions:
    DEFAULT_OPTIONS = {
      "max_tokens": 4000,
      "temperature": 0.7,
      "top_k": -1,
      "top_p": -1
    }

    def __init__(self, options={}):
        self.__init_defaults()

        self.options_set = []
        self.update_options(self.defaults)
        self.update_options(options)

    def update_options(self, options):
        for key in options.keys():
          if options[key] != None:
            if key in ALLOWED_OPTIONS:
                if key not in self.options_set:
                    self.options_set.append(key)
               
                setattr(self, key, options[key])

    def description(self):
        return " ".join([f"{key}={self.option(key)}" for key in self.options_set])

    def option(self, key):
        return getattr(self, key)

    def __repr__(self):
        return self.description()

    def to_dict(self):
        dict = {}

        for key in self.options_set:
            dict[key] = self.option(key)

        return dict

    def __config_key_for_option_key(self, option_key):
      return f"DEFAULT_{option_key.upper()}"
    
    def __init_defaults(self):
      self.defaults = ModelOptions.DEFAULT_OPTIONS.copy()

      for option_key in ALLOWED_OPTIONS:
        config_key = self.__config_key_for_option_key(option_key)
        defaults_value = config.get(config_key)
        
        if defaults_value:
          if option_key == "temperature":
            target_value = float(defaults_value)
          else:
            target_value = int(defaults_value)

          self.defaults[option_key] = target_value
