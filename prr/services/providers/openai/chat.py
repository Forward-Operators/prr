import openai

from prr.runner.request import ServiceRequest
from prr.runner.response import ServiceResponse
from prr.utils.config import load_config

config = load_config()
openai.api_key = config["OPENAI_API_KEY"]


# OpenAI model provider class
class ServiceOpenAIChat:
    provider = "openai"
    service = "chat"

    def run(self, prompt, service_config):
        messages = prompt.template.render_messages()

        service_request = ServiceRequest(service_config, {"messages": messages})

        options = service_config.options

        completion = openai.ChatCompletion.create(
            model=service_config.model_name(),
            messages=messages,
            temperature=options.temperature,
            max_tokens=options.max_tokens,
        )

        usage = completion.usage

        choices = completion.choices
        first_choice = choices[0]

        completion_content = first_choice.message.content

        service_response = ServiceResponse(
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

        return service_request, service_response
