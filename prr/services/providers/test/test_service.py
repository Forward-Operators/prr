from prr.services.service_base import ServiceBase
from prr.utils.response import ServiceResponse


# Test/mock service provider class
class ServiceTest(ServiceBase):
    provider = "test_provider"
    service = "test_service"

    # options we take into account
    options = ["max_tokens", "temperature"]

    def run(self):
        completion_content = f"""TEST COMPLETION. INPUT RECEIVED:
model: {self.service_config.model_name()}
messages: {self.request.prompt_content}
temperature: {self.option("temperature")}
max_tokens: {self.option("max_tokens")}
"""

        self.response = ServiceResponse(
            completion_content,
            {
                "tokens_used": 666,
                "completion_tokens": 666,
                "prompt_tokens": 12345,
                "total_tokens": 31337,
                "finish_reason": "stop",
            },
        )

        return self.request, self.response

    def render_prompt(self):
        return self.prompt.render_messages(self.prompt_args)
