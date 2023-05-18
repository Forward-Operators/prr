# https://console.anthropic.com/docs/api/reference
# https://github.com/anthropics/anthropic-sdk-python/tree/main/examples

import os

import anthropic

from prr.config import load_config
from prr.request import ServiceRequest
from prr.response import ServiceResponse

config = load_config()

# https://console.anthropic.com/docs/api/reference


# Anthropic model provider class
class ServiceAnthropicComplete:
    provider = "anthropic"
    service = "complete"

    def run(self, prompt, service_config):
        self.service_config = service_config
        options = self.service_config.options
        self.prompt = prompt

        prompt_text = self.prompt_text()

        client = anthropic.Client(config.get("ANTHROPIC_API_KEY", None))

        service_request = ServiceRequest(self.service_config, prompt_text)

        response = client.completion(
            prompt=prompt_text,
            stop_sequences=[anthropic.HUMAN_PROMPT],
            model=service_config.model_name(),
            max_tokens_to_sample=options.max_tokens,
            temperature=options.temperature,
            top_p=options.top_p,
            top_k=options.top_k,
        )

        completion_tokens = anthropic.count_tokens(response["completion"])
        prompt_tokens = anthropic.count_tokens(prompt_text)
        total_tokens = prompt_tokens + completion_tokens

        service_response = ServiceResponse(
            response["completion"],
            {
                "tokens_used": total_tokens,
                "prompt_tokens": anthropic.count_tokens(prompt_text),
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens,
                "truncated": response["truncated"],
                "stop_reason": response["stop_reason"],
                "log_id": response["log_id"],
            },
        )

        return service_request, service_response

    def prompt_text(self):
        messages = self.prompt.messages

        prompt_text = ""

        # prefer messages from prompt if they exist
        if messages:
            for message in messages:
                if message["role"] != "assistant":
                    prompt_text += " " + message["content"]

        else:
            prompt_text = self.prompt.text()

        return f"{anthropic.HUMAN_PROMPT} {prompt_text}{anthropic.AI_PROMPT}"
