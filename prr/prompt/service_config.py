from prr.prompt.model_options import ModelOptions


class ServiceConfig:
    def __init__(self, name, model, options=None):
        self.name = name  # service config name, e.g. "mygpt5"
        self.model = model  # full model path, e.g. "openai/chat/gpt-5"
        self.options = ModelOptions(options or {})

    def process_option_overrides(self, option_overrides):
        self.options.update_options(option_overrides)

    # which model to use with the service
    # like "gpt-4.5-turbo" or "claude-v1.3-100k"
    def model_name(self):
        return self.model.split("/")[-1]

    # which service so use
    # like "openai/chat" or "anthropic/complete"
    def service_key(self):
        return "/".join(self.model.split("/")[:-1])

    def to_dict(self):
        return {"model": self.config_name(), "options": self.options.to_dict()}
