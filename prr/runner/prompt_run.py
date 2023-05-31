import time

from prr.runner.prompt_run_result import PromptRunResult


# takes prompt and model config, finds provider, runs the prompt
class PromptRun:
    def __init__(self, prompt, service_class, service_config):
        self.prompt = prompt
        self.service_class = service_class
        self.service_config = service_config

        self.result = PromptRunResult(self.prompt, self.service_config)

        self.service = self.service_class(self.prompt, self.service_config)

    def run(self):

        self.result.before_run()

        request, response = self.service.run()

        self.result.after_run()

        self.result.update_with_request(request)
        self.result.update_with_response(response)

        return self.result
