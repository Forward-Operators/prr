from elevenlabs import generate, set_api_key

from prr.services.service_base import ServiceBase
from prr.utils.config import load_config
from prr.utils.response import ServiceResponse

config = load_config()
set_api_key(config.get("ELEVENLABS_API_KEY", None))


# Eleven Labs model provider class
# models: "eleven_monolingual_v1", "eleven_multilingual_v1"
class ServiceElevenLabsTTS(ServiceBase):
    provider = "elevenlabs"
    service = "tts"
    options = ["voice"]

    def run(self):
        audio = generate(
            text=self.request.prompt_content,
            voice=self.option("voice"),
            model=self.service_config.model_name(),
        )

        self.response = ServiceResponse(audio)

        return self.request, self.response
