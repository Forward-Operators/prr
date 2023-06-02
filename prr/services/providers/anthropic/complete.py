# https://console.anthropic.com/docs/api/reference
# https://github.com/anthropics/anthropic-sdk-python/tree/main/examples

import os

import anthropic

from prr.runner.response import ServiceResponse
from prr.utils.config import load_config
from prr.services.service_base import ServiceBaseUnstructuredPrompt


config = load_config()
client = anthropic.Client(config.get("ANTHROPIC_API_KEY", None))

# Anthropic model provider class
class ServiceAnthropicComplete(ServiceBaseUnstructuredPrompt):
    provider = "anthropic"
    service = "complete"
    options = ["max_tokens", "temperature", "top_k", "top_p"]

    def run(self):
        result = client.completion(
            prompt=self.request.prompt_content,
            stop_sequences=[anthropic.HUMAN_PROMPT],
            model=self.service_config.model_name(),
            max_tokens_to_sample=self.option('max_tokens'),
            temperature=self.option('temperature'),
            top_p=self.option('top_p'),
            top_k=self.option('top_k'),
        )

        completion_tokens = anthropic.count_tokens(result["completion"])
        prompt_tokens = anthropic.count_tokens(self.request.prompt_content)
        total_tokens = prompt_tokens + completion_tokens

        self.response = ServiceResponse(
            result["completion"],
            {
                "tokens_used": total_tokens,
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens,
                "truncated": result["truncated"],
                "stop_reason": result["stop_reason"],
                "log_id": result["log_id"],
            },
        )

        return self.request, self.response

    # define render prompt to change how the prompt is rendered
    def render_prompt(self):
        prompt_text = ""

        # prefer messages from template if they exist
        if self.prompt.template.messages:
            for message in self.prompt.template.messages:
                if message.role != "assistant":
                    prompt_text += "\n" + message.render_text()

        else:
            prompt_text = self.prompt.template.render_text()

        return f"{anthropic.HUMAN_PROMPT}{prompt_text}{anthropic.AI_PROMPT}"
