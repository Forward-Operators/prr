DEFAULT_OPTIONS = {"temperature": 1.0, "top_k": -1, "top_p": -1, "max_tokens": 4000}

ALLOWED_OPTIONS = DEFAULT_OPTIONS.keys()


class ModelOptions:
    def __init__(self, options={}):
        self.options_set = []
        self.update_options(DEFAULT_OPTIONS)
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
