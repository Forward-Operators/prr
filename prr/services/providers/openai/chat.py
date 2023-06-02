import openai

from prr.runner.response import ServiceResponse
from prr.utils.config import load_config

from prr.services.service_base import ServiceBaseStructuredPrompt

config = load_config()
openai.api_key = config.get("OPENAI_API_KEY", None)

# OpenAI model provider class
class ServiceOpenAIChat(ServiceBaseStructuredPrompt):
    provider = "openai"
    service = "chat"

    # options we take into account
    options = ["max_tokens", "temperature"]
    
    def run(self):
        completion = openai.ChatCompletion.create(
            model=self.service_config.model_name(),
            messages=self.request.prompt_content,
            temperature=self.option('temperature'),
            max_tokens=self.option('max_tokens'),
        )

        usage = completion.usage
        choices = completion.choices

        first_choice = choices[0]
        completion_content = first_choice.message.content

        self.response = ServiceResponse(
            completion_content,
            {
                "choices": len(choices),
                "tokens_used": usage.total_tokens,
                "completion_tokens": usage.completion_tokens,
                "prompt_tokens": usage.prompt_tokens,
                "total_tokens": usage.total_tokens,
                "finish_reason": first_choice.finish_reason,
            },
        )

        return self.request, self.response
