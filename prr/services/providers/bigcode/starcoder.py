from huggingface_hub import Repository
from text_generation import Client

from prr.runner.request import ServiceRequest
from prr.runner.response import ServiceResponse
from prr.utils.config import load_config

from prr.services.service_base import ServiceBaseUnstructuredPrompt

config = load_config()

HF_TOKEN = config.get("HF_TOKEN", None)
API_URL = "https://api-inference.huggingface.co/models/bigcode/starcoder"

FIM_PREFIX = "<fim_prefix>"
FIM_MIDDLE = "<fim_middle>"
FIM_SUFFIX = "<fim_suffix>"

FIM_INDICATOR = "<FILL_HERE>"


client = Client(
    API_URL,
    headers={"Authorization": f"Bearer {HF_TOKEN}"},
)

class ServiceBigcodeStarcoder(ServiceBaseUnstructuredPrompt):
    provider = "bigcode"
    service = "starcoder"
    options = ["temperature", "max_tokens", "top_p", "repetition_penalty"]

    def run(self):
        completion = client.generate(
            self.request.prompt_content,
            temperature=self.option('temperature'),
            max_new_tokens=self.option('max_tokens'),
            top_p=self.option('top_p'),
            repetition_penalty=self.option('repetition_penalty')
        )

        self.response = ServiceResponse(
            completion.generated_text,
            {
                "tokens_used": completion.details.generated_tokens,
                "stop_reason": str(completion.details.finish_reason),
            },
        )

        return self.request, self.response
