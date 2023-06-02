from prr.runner.request import ServiceRequest


class ServiceBase:
    def __init__(self, prompt, prompt_args, service_config):
        self.prompt = prompt
        self.prompt_args = prompt_args
        self.service_config = service_config

        self.request = ServiceRequest(
          self.service_config, 
          self.render_prompt(), 
          self.request_options()
        )

    def request_options(self):
        return self.service_config.options.select(self.__class__.options)

    def option(self, option_name):
        return self.request.options.value(option_name)

class ServiceBaseUnstructuredPrompt(ServiceBase):
    def render_prompt(self):
        return self.prompt.render_text(self.prompt_args)

class ServiceBaseStructuredPrompt(ServiceBase):
    def render_prompt(self):
        return self.prompt.render_messages(self.prompt_args)
