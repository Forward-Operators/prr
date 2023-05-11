import os

import jinja2
import yaml
from jinja2 import meta

from .service_config import ServiceConfig


# parse something like:
#
# services:
#   gpt35crazy:
#     model: 'openai/chat/gpt-3.5-turbo'
#     options:
#       temperature: 0.99
#   claudev1smart:
#     model: 'anthropic/complete/claude-v1'
#     options:
#       temperature: 0
#   options:
#     temperature: 0.7
#     max_tokens: 64
def parse_specifically_configured_services(services_config):
    options = services_config.get("options")
    services_config.pop("options")

    service_names = services_config.keys()

    services = {}

    for service_name in service_names:
        service_config = services_config[service_name]
        model = service_config["model"]
        service_config.pop("model")

        merged_options = options.copy()

        if service_config["options"]:
            service_options = service_config["options"]
            merged_options.update(service_options)

        services[service_name] = ServiceConfig(model, merged_options)

    return services


# parse something like:
#
# services:
#   models:
#     - 'openai/chat/gpt-3.5-turbo'
#     - 'anthropic/complete/claude-v1'
#   options:
#     temperature: 0.7
#     max_tokens: 100
#     top_p: 1.0
#     top_k: 40
def parse_generally_configured_services(services_config):
    options = services_config.get("options")
    models = services_config.get("models")

    services = {}

    for model in models:
        services[model] = ServiceConfig(model, options)

    return services


def parse_config_into_services(services_config):
    if services_config.get("models"):
        return parse_generally_configured_services(services_config)
    else:
        return parse_specifically_configured_services(services_config)


class Prompt:
    def __init__(self, path, args=None):
        self.path = None
        self.messages = None
        self.template = None
        self.services = {}
        self.args = args
        # TODO/FIXME: should also include jinja includes
        self.dependency_files = []

        template_loader = jinja2.FileSystemLoader(searchpath=os.path.dirname(path))
        self.template_env = jinja2.Environment(loader=template_loader)

        root, extension = os.path.splitext(path)

        if extension == ".yaml":
            self.load_yaml_file(path)
        else:
            self.load_text_file(path)

    def configured_service_names(self):
        if self.services:
            return list(self.services.keys())

        return []

    def parse_messages(self, messages):
        # expand content_file field in messages
        self.messages = []
        self.dependency_files = []
        root_path = os.path.dirname(self.path)

        if messages:
            for message in messages:
                if message.get("content_file"):
                    updated_message = message.copy()
                    file_path = os.path.join(
                        root_path, updated_message.pop("content_file")
                    )

                    with open(file_path, "r") as f:
                        updated_message.update({"content": f.read()})
                        self.messages.append(updated_message)
                        self.dependency_files.append(file_path)
                else:
                    self.messages.append(message)

    def add_dependency_files_from_jinja_template(self, jinja_template_content):
        parsed_content = self.template_env.parse(jinja_template_content)
        referenced_templates = meta.find_referenced_templates(parsed_content)

        for referenced_template in referenced_templates:
            template_path = os.path.join(
                os.path.dirname(self.path), referenced_template
            )
            self.dependency_files.append(template_path)

    def parse_services(self, services_config):
        self.services = parse_config_into_services(services_config)

    def parse_prompt_config(self, prompt_config):
        if prompt_config.get("messages"):
            self.parse_messages(prompt_config["messages"])
        elif prompt_config.get("content"):
            self.template = self.load_jinja_template_from_string(
                prompt_config["content"]
            )
        elif prompt_config.get("content_file"):
            self.template = self.load_jinja_template_from_file(
                prompt_config["content_file"]
            )

    def config_for_service(self, service_name):
        if self.services:
            if self.services.get(service_name):
                return self.services[service_name]

        return ServiceConfig(service_name)

    def load_yaml_file(self, path):
        with open(path, "r") as stream:
            try:
                file_contents = self.deal_with_shebang_line(stream)
                data = yaml.safe_load(file_contents)
                self.path = path
            except yaml.YAMLError as exc:
                print(exc)

            if data:
                if data["services"]:
                    self.parse_services(data["services"])
                if data["prompt"]:
                    self.parse_prompt_config(data["prompt"])

    def deal_with_shebang_line(self, stream):
        file_contents = stream.readlines()

        # if the file starts with a shebang, like #!/usr/bin/prr, omit it
        if file_contents[0].startswith("#!/"):
            if file_contents[1] == "\n":
                # allow for one empty line below the shebang
                file_contents = file_contents[2:]
            else:
                file_contents = file_contents[1:]

        return "".join(file_contents)

    def load_jinja_template_from_string(self, content):
        self.add_dependency_files_from_jinja_template(content)
        return self.template_env.from_string(content)

    def load_jinja_template_from_file(self, template_subpath):
        try:
            with open(
                os.path.join(os.path.dirname(self.path), template_subpath), "r"
            ) as stream:
                self.add_dependency_files_from_jinja_template(stream.read())

                return self.template_env.get_template(template_subpath)
        except FileNotFoundError:
            print(f"Could not find template file: {template_subpath}")
            exit(-1)

    def load_text_file(self, path):
        self.path = path

        with open(path, "r") as stream:
            file_contents = self.deal_with_shebang_line(stream)
            self.template = self.template_env.from_string(file_contents)

    def message_text_description(self, message):
        name = message.get("name")
        role = message.get("role")
        content = message.get("content")

        if name:
            return f"{name} ({role}): {content}"
        else:
            return f"{role}: {content}"

    def text(self):
        if self.messages:
            return "\n".join(
                [self.message_text_description(msg) for msg in self.messages]
            )

        if self.args:
            return self.template.render({"prompt_args": self.args})

        return self.template.render()

    def text_len(self):
        return len(self.text())

    def dump(self):
        return yaml.dump({"text": self.text(), "messages": self.messages})

    def text_abbrev(self, max_len=25):
        if self.text_len() > max_len:
            str = self.text()[0:max_len] + "..."
        else:
            str = self.text()

        return str.replace("\n", " ").replace("  ", " ")
