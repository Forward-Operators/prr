import openai

from prr.services.service_base import ServiceBase
from prr.utils.config import ensure_api_key, load_config
from prr.utils.response import ServiceResponse

config = load_config()


# OpenAI model provider class
class ServiceOpenAIChat(ServiceBase):
    provider = "openai"
    service = "chat"

    # options we take into account
    options = ["max_tokens", "temperature"]

    def run(self):
        openai.api_key = ensure_api_key(config, "OPENAI_API_KEY")

        completion = openai.ChatCompletion.create(
            model=self.service_config.model_name(),
            messages=self.request.prompt_content,
            temperature=self.option("temperature"),
            max_tokens=self.option("max_tokens"),
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

    def render_prompt(self):
        return self.prompt.render_messages(self.prompt_args)
