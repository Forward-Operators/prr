from huggingface_hub import Repository
from text_generation import Client

from prr.runner.request import ServiceRequest
from prr.runner.response import ServiceResponse
from prr.utils.config import load_config

config = load_config()

HF_TOKEN = config.get("HF_TOKEN", None)
API_URL = "https://api-inference.huggingface.co/models/bigcode/starcoder"

FIM_PREFIX = "<fim_prefix>"
FIM_MIDDLE = "<fim_middle>"
FIM_SUFFIX = "<fim_suffix>"

FIM_INDICATOR = "<FILL_HERE>"


class ServiceBigcodeStarcoder:
    provider = "bigcode"
    service = "starcoder"

    def run(self, prompt, service_config):
        self.service_config = service_config
        options = self.service_config.options
        self.prompt = prompt

        client = Client(
            API_URL,
            headers={"Authorization": f"Bearer {HF_TOKEN}"},
        )

        options = self.service_config.options

        prompt_text = prompt.template_text()

        service_request = ServiceRequest(service_config, prompt_text)

        response = client.generate(
            prompt_text,
            temperature=options.temperature,
            max_new_tokens=options.max_tokens,
            top_p=options.top_p,
            # repetition_penalty=options.repetition_penalty,
        )

        service_response = ServiceResponse(
            response.generated_text,
            {
                "tokens_used": response.details.generated_tokens,
                "stop_reason": response.details.finish_reason,
            },
        )

        return service_request, service_response
