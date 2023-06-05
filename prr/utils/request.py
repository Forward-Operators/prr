import yaml


# request we're sending to the service - prompts rendered, options parsed
class ServiceRequest:
    def __init__(self, service_config, rendered_prompt_content, options):
        self.service_config = service_config
        self.prompt_content = rendered_prompt_content
        self.options = options

    def to_dict(self):
        return {
            "model": self.service_config.model,
            "options": self.options.to_dict(),
        }

    def prompt_text(self, max_len=0):
        if isinstance(self.prompt_content, str):
            text = self.prompt_content
        else:
            text = yaml.dump(self.prompt_content)

        if max_len > 0 and len(text) > max_len:
            text = text[0:max_len] + "..."

            return text.replace("\n", " ").replace("  ", " ")

        return text
