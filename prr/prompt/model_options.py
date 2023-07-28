from prr.utils.config import load_config

config = load_config()


class ModelOptions:
    DEFAULT_OPTIONS = {"max_tokens": 4000, "temperature": 0.7, "top_k": -1, "top_p": -1}

    def __init__(self, options={}, use_defaults=True):
        self.__init_defaults()

        self.options_set = []

        if use_defaults:
            self.update_options(self.defaults)

        self.update_options(options)

    def select(self, option_keys):
        _options = {}

        for key in option_keys:
            if key in self.options_set:
                _options[key] = self.value(key)

        return ModelOptions(_options, False)

    def update_options(self, options):
        if options == None:
            return

        for key in options.keys():
            if options[key] != None:
                if key not in self.options_set:
                    self.options_set.append(key)

                setattr(self, key, options[key])

    def description(self):
        return " ".join([f"{key}={self.value(key)}" for key in self.options_set])

    def value(self, key):
        if hasattr(self, key) and key in self.options_set:
            return getattr(self, key)

        return None

    def __repr__(self):
        return self.description()

    def to_dict(self):
        dict = {}

        for key in self.options_set:
            dict[key] = self.value(key)

        return dict

    def __config_key_for_option_key(self, option_key):
        return f"DEFAULT_{option_key.upper()}"

    def __init_defaults(self):
        self.defaults = ModelOptions.DEFAULT_OPTIONS.copy()

        for option_key in ModelOptions.DEFAULT_OPTIONS.keys():
            config_key = self.__config_key_for_option_key(option_key)
            defaults_value = config.get(config_key)

            if defaults_value:
                if option_key == "temperature":
                    target_value = float(defaults_value)
                else:
                    target_value = int(defaults_value)

                self.defaults[option_key] = target_value
