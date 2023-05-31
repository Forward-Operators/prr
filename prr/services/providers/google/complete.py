from google.cloud import aiplatform
from vertexai.preview.language_models import TextGenerationModel

from prr.runner.response import ServiceResponse
from prr.utils.config import load_config
from prr.services.service_base import ServiceBaseUnstructuredPrompt


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


class ServiceGoogleComplete(ServiceBaseUnstructuredPrompt):
    provider = "google"
    service = "complete"
    options = ["max_tokens", "temperature", "top_k", "top_p"]

    def run(self):
        client = TextGenerationModel.from_pretrained(self.service_config.model_name())

        result = client.predict(
            prompt_text,
            max_output_tokens=self.options('max_tokens'),
            temperature=self.options('temperature'),
            top_k=self.options('top_k'),
            top_p=self.options('top_p'),
        )

        self.response = ServiceResponse(
            str(result),
            {
                "details": result,
            },
        )

        return self.request, self.response

    def render_prompt(self):
        messages = self.prompt.messages

        prompt_text = ""

        if messages:
            for message in messages:
                if message["role"] != "assistant":
                    prompt_text += " " + message["content"]

        else:
            prompt_text = self.prompt.text()

        return messages
