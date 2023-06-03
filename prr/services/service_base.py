from prr.utils.request import ServiceRequest


class ServiceBase:
    def __init__(self, prompt, prompt_args, service_config):
        self.prompt = prompt
        self.prompt_args = prompt_args
        self.service_config = service_config

        self.request = ServiceRequest(
            self.service_config, self.render_prompt(), self.render_options()
        )

    def render_options(self):
        return self.service_config.options.select(self.__class__.options)

    def render_prompt(self):
        return self.prompt.render_text(self.prompt_args)

    def option(self, option_name):
        return self.request.options.value(option_name)
