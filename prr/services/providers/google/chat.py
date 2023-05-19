from google.cloud import aiplatform
from vertexai.preview.language_models import ChatModel, InputOutputTextPair

from prr.config import load_config
from prr.request import ServiceRequest
from prr.response import ServiceResponse

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


class ServiceGoogleChat:
    provider = "google"
    service = "chat"

    def run(self, prompt, service_config):
        self.service_config = service_config
        options = self.service_config.options
        self.prompt = prompt

        messages = self.messages_from_prompt()

        model = ChatModel.from_pretrained(self.service_config.model_name())

        service_request = ServiceRequest(self.service_config, {"messages": messages})

        parameters = {
            "temperature": options.temperature,
            "max_output_tokens": options.max_tokens,
            "top_p": options.top_p,
            "top_k": options.top_k,
        }

        chat = model.start_chat(
            context=f"""{self.context_from_messages()}""",
            examples=[],
        )

        response = chat.send_message(
            f"""{self.message_from_messages()}""", **parameters
        )

        service_response = ServiceResponse(response.text, {})

        return service_request, service_response

    def messages_from_prompt(self):
        messages = self.prompt.messages

        # prefer messages in prompt if they exist
        if messages:
            return messages

        return [{"role": "user", "content": self.prompt.text()}]

    def context_from_messages(self):
        messages = self.prompt.messages

        if messages:
            for message in messages:
                if message["role"] == "system":
                    context = message["content"]
        else:
            context = None

        return context

    def examples_from_messages(self):
        messages = self.prompt.messages

        if messages:
            examples = []
            for message in messages:
                if message["role"] == "examples":
                    examples.append(
                        InputOutputTextPair(message["input"], message["output"])
                    )
        else:
            examples = []

        return examples

    def message_from_messages(self):
        messages = self.prompt.messages

        if messages:
            for message in messages:
                if message["role"] == "user":
                    message = message["content"]
        else:
            message = None

        return message
