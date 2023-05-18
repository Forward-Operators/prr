from google.cloud import aiplatform
from vertexai.preview.language_models import TextGenerationModel

from prr.config import load_config
from prr.request import ServiceRequest
from prr.response import ServiceResponse

config = load_config()

aiplatform.init(
    # your Google Cloud Project ID or number
    # environment default used is not set
    project=config.get("GOOGLE_PROJECT", None),
    # the Vertex AI region you will use
    # defaults to us-central1
    location=config.get("GOOGLE_LOCATION", None),
    # custom google.auth.credentials.Credentials
    # environment default creds used if not set
    # credentials=config[my_credentials],
)


class ServiceGoogleComplete:
    provider = "google"
    service = "complete"

    def run(self, prompt, service_config):
        self.service_config = service_config
        options = self.service_config.options
        self.prompt = prompt

        prompt_text = self.prompt_text()

        client = TextGenerationModel.from_pretrained(self.service_config.model_name())

        service_request = ServiceRequest(self.service_config, prompt_text)

        options = self.service_config.options

        response = client.predict(
            prompt_text,
            max_output_tokens=options.max_tokens,
            temperature=options.temperature,
            top_k=options.top_k,
            top_p=options.top_p,
        )

        service_response = ServiceResponse(
            str(response),
            {
                "details": response,
            },
        )

        return service_request, service_response

    def prompt_text(self):
        messages = self.prompt.messages

        prompt_text = ""

        if messages:
            for message in messages:
                if message["role"] != "assistant":
                    prompt_text += " " + message["content"]

        else:
            prompt_text = self.prompt.text()

        return messages
