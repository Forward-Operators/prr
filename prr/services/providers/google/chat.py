from google.cloud import aiplatform
from vertexai.preview.language_models import ChatModel, InputOutputTextPair

from prr.utils.response import ServiceResponse
from prr.utils.config import load_config
from prr.services.service_base import ServiceBaseUnstructuredPrompt

config = load_config()

aiplatform.init(
    # your Google Cloud Project ID or number
    # environment default used is not set
    project=config.get("GOOGLE_PROJECT"),
    # the Vertex AI region you will use
    # defaults to us-central1
    location=config.get("GOOGLE_LOCATION"),
    # custom google.auth.credentials.Credentials
    # environment default creds used if not set
    # credentials=config[my_credentials],
)


class ServiceGoogleChat(ServiceBaseStructuredPrompt):
    provider = "google"
    service = "chat"
    options = ["max_tokens", "temperature", "top_k", "top_p"]

    def run(self):
        model = ChatModel.from_pretrained(self.service_config.model_name())

        parameters = {
            "temperature": self.option('temperature'),
            "max_output_tokens": self.option('max_tokens'),
            "top_p": self.option('top_p'),
            "top_k": self.option('top_k'),
        }

        # TODO: examples (use 'assistant' role for that)
        chat = model.start_chat(
            context=f"""{self.context_from_messages()}""",
            examples=[],
        )

        response = chat.send_message(
            f"""{self.message_from_messages()}""", **parameters
        )

        self.response = ServiceResponse(response.text, {})

        return self.request, self.response

    # define render prompt to change how the prompt is rendered
    def render_prompt(self):
        _output = {
          "context": "",
          "messages": []
        }

        # TODO: this should not reach so deep
        if self.request.prompt.template.messages:
            for message in self.prompt.template.messages:
                if message.role == "system":
                    _output["context"] += "\n" + message.render_text()
                elif message.role == "user":
                    _msg = {}
                    _msg['author'] = message.role
                    _msg['content'] = message.render_text()

                    _output.messages.append(_msg)

        return _output