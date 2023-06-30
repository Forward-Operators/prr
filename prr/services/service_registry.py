# main registry, where services are being... registered
# and looked up for upon execution
class ServiceRegistry:
    def __init__(self):
        self.services = {}

    def register(self, service_class):
        key = f"{service_class.provider}/{service_class.service}"
        self.services[key] = service_class

    def register_all_services(self):
        from prr.services.providers.anthropic.complete import ServiceAnthropicComplete
        from prr.services.providers.bigcode.starcoder import ServiceBigcodeStarcoder
        from prr.services.providers.elevenlabs.tts import ServiceElevenLabsTTS
        from prr.services.providers.google.chat import ServiceGoogleChat
        from prr.services.providers.google.complete import ServiceGoogleComplete
        from prr.services.providers.openai.chat import ServiceOpenAIChat
        from prr.services.providers.test.test_service import ServiceTest

        self.register(ServiceOpenAIChat)
        self.register(ServiceAnthropicComplete)
        self.register(ServiceBigcodeStarcoder)
        self.register(ServiceGoogleComplete)
        self.register(ServiceGoogleChat)
        self.register(ServiceElevenLabsTTS)
        self.register(ServiceTest)

    def service_for_service_config(self, service_config):
        key = service_config.service_key()
        return self.services[key]
