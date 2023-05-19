import openai

from prr.config import load_config
from prr.request import ServiceRequest
from prr.response import ServiceResponse

config = load_config()
openai.api_key = config.get("OPENAI_API_KEY", None)


# OpenAI model provider class
class ServiceOpenAIChat:
    provider = "openai"
    service = "chat"

    def run(self, prompt, service_config):
        self.prompt = prompt
        self.service_config = service_config

        messages = self.messages_from_prompt()

        service_request = ServiceRequest(self.service_config, {"messages": messages})

        options = self.service_config.options

        completion = openai.ChatCompletion.create(
            model=self.service_config.model_name(),
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

    def messages_from_prompt(self):
        messages = self.prompt.messages

        # prefer messages in prompt if they exist
        if messages:
            return messages

        return [{"role": "user", "content": self.prompt.text()}]
