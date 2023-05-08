import time

from .prompt_run_result import PromptRunResult


# takes prompt and model config, finds provider, runs the prompt
class PromptRun:
    def __init__(self, prompt, service, service_config):
        self.prompt = prompt
        self.service = service
        self.service_config = service_config

    def run(self):
        result = PromptRunResult(self.prompt, self.service_config)

        result.before_run()

        request, response = self.service.run(self.prompt, self.service_config)

        result.after_run()

        result.update_with_request(request)
        result.update_with_response(response)

        return result
