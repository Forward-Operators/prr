from google.cloud import aiplatform
from vertexai.preview.language_models import ChatModel, InputOutputTextPair

from prr.services.service_base import ServiceBase
from prr.utils.config import ensure_api_key, load_config
from prr.utils.response import ServiceResponse

config = load_config()


class ServiceGoogleChat(ServiceBase):
    provider = "google"
    service = "chat"
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

        model = ChatModel.from_pretrained(self.service_config.model_name())

        parameters = {
            "temperature": self.option("temperature"),
            "max_output_tokens": self.option("max_tokens"),
            "top_p": self.option("top_p"),
            "top_k": self.option("top_k"),
        }

        # TODO: support examples
        chat = model.start_chat(
            context=self.request.prompt_content["context"],
            examples=[],
        )

        response = chat.send_message(
            self.request.prompt_content["messages"], **parameters
        )

        self.response = ServiceResponse(response.text, {})

        return self.request, self.response

    def render_message(self, message):
        return {
            "author": "bot" if message.is_assistant() else "user",
            "content": message.render_text(self.prompt_args),
        }

    # define render prompt to change how the prompt is rendered
    def render_prompt(self):
        context_messages = []
        chat_messages = []

        # TODO: this should not reach so deep
        if self.prompt.template.messages:
            for message in self.prompt.template.messages:
                if message.is_system():
                    context_messages.append(message)
                else:
                    chat_messages.append(message)

        context_text = "\n".join(
            [m.render_text(self.prompt_args) for m in context_messages]
        )
        messages = [self.render_message(m) for m in chat_messages]

        return {
            "context": context_text,
            "messages": messages,
        }
