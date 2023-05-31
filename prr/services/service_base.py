from prr.runner.request import ServiceRequest


class ServiceBase:
    def __init__(self, prompt, service_config):
        self.prompt = prompt
        self.service_config = service_config

        self.request = ServiceRequest(
          self.service_config, 
          self.render_prompt(), 
          self.request_options()
        )

    def request_options(self):
        return self.service_config.options.select(self.__class__.options)

    def option(self, option_name):
        return self.request.options.option(option_name)

class ServiceBaseUnstructuredPrompt(ServiceBase):
    def render_prompt(self):
        return self.prompt.template_text()

class ServiceBaseStructuredPrompt(ServiceBase):
    def render_prompt(self):
        return self.prompt.template.render_messages(),
