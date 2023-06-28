import time

from prr.runner.prompt_run_result import PromptRunResult


# takes prompt and model config, finds provider, runs the prompt
class PromptRun:
    def __init__(self, prompt, prompt_args, service_class, service_config):
        self.prompt = prompt
        self.prompt_args = prompt_args

        self.service_class = service_class
        self.service_config = service_config

        self.result = PromptRunResult(self.prompt, self.service_config)

        self.service = self.service_class(
            self.prompt, self.prompt_args, self.service_config
        )

    def run(self):
        self.result.before_run()

        request, response = self.service.run()

        self.result.after_run()

        self.result.update_with_request(request)
        self.result.update_with_response(response)

        return self.result

    def __str__(self):
        return f"PromptRun(prompt={self.prompt}, prompt_args={self.prompt_args}, service_class={self.service_class}, service_config={self.service_config}, result={self.result})"
