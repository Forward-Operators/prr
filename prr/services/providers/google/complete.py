from google.cloud import aiplatform
from vertexai.preview.language_models import TextGenerationModel

from prr.services.service_base import ServiceBase
from prr.utils.config import ensure_api_key, load_config
from prr.utils.response import ServiceResponse

config = load_config()


class ServiceGoogleComplete(ServiceBase):
    provider = "google"
    service = "complete"
    options = ["max_tokens", "temperature", "top_k", "top_p"]

    def run(self):
        aiplatform.init(
            # your Google Cloud Project ID or number
            # environment default used is not set
            project=ensure_api_key(config, "GOOGLE_PROJECT"),
            # the Vertex AI region you will use
            # defaults to us-central1
            location=ensure_api_key(config, "GOOGLE_LOCATION"),
            # custom google.auth.credentials.Credentials
            # environment default creds used if not set
            # credentials=config[my_credentials],
        )

        client = TextGenerationModel.from_pretrained(self.service_config.model_name())

        result = client.predict(
            prompt_text,
            max_output_tokens=self.option("max_tokens"),
            temperature=self.option("temperature"),
            top_k=self.option("top_k"),
            top_p=self.option("top_p"),
        )

        self.response = ServiceResponse(
            str(result),
            {
                "details": result,
            },
        )

        return self.request, self.response
