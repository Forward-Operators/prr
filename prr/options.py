ALLOWED_OPTIONS = ["max_tokens", "temperature", "top_k", "top_p"]

# user-level defaults
# TODO/FIXME: make it user-configurable in ~/.prr*
DEFAULT_OPTIONS = {
  "max_tokens": 4000,
  "temperature": 0.7,
  "top_k": -1,
  "top_p": -1
}

class ModelOptions:
    defaults = DEFAULT_OPTIONS

    def __init__(self, options={}):
        self.options_set = []
        self.update_options(ModelOptions.defaults)
        self.update_options(options)

    def update_options(self, options):
        for key in options.keys():
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
