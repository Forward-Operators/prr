from huggingface_hub import Repository
from text_generation import Client

from prr.services.service_base import ServiceBase
from prr.utils.config import ensure_api_key, load_config
from prr.utils.request import ServiceRequest
from prr.utils.response import ServiceResponse

config = load_config()

API_URL = "https://api-inference.huggingface.co/models/bigcode/starcoder"

FIM_PREFIX = "<fim_prefix>"
FIM_MIDDLE = "<fim_middle>"
FIM_SUFFIX = "<fim_suffix>"

FIM_INDICATOR = "<FILL_HERE>"


class ServiceBigcodeStarcoder(ServiceBase):
    provider = "bigcode"
    service = "starcoder"
    options = ["temperature", "max_tokens", "top_p", "repetition_penalty"]

    def run(self):
        HF_TOKEN = ensure_api_key(config, "HF_TOKEN")

        client = Client(
            API_URL,
            headers={"Authorization": f"Bearer {HF_TOKEN}"},
        )

        completion = client.generate(
            self.request.prompt_content,
            temperature=self.option("temperature"),
            max_new_tokens=self.option("max_tokens"),
            top_p=self.option("top_p"),
            repetition_penalty=self.option("repetition_penalty"),
        )

        self.response = ServiceResponse(
            completion.generated_text,
            {
                "tokens_used": completion.details.generated_tokens,
                "stop_reason": str(completion.details.finish_reason),
            },
        )

        return self.request, self.response
