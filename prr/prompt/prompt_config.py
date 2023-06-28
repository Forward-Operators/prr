import yaml

from prr.prompt.prompt_template import PromptTemplateMessages, PromptTemplateSimple
from prr.prompt.service_config import ServiceConfig


class PromptConfig:
    # raw_config_content is text to be parsed into YAML
    def __init__(self, search_path=".", filename=None):
        # where are we supposed to look for referenced files
        self.search_path = search_path

        # "foo" or "foo.yaml" - no path
        self.filename = filename

        # template: (PromptTemplate)
        self.template = None

        # services: (ServiceConfig)
        self.services = {}

        # version: 1
        self.version = None

    def render_text(self, prompt_args=None):
        return self.template.render_text(prompt_args)

    def render_messages(self, prompt_args=None):
        return self.template.render_messages(prompt_args)

    # raw YAML file
    def load_from_config_contents(self, raw_config_content):
        # raw YAML string
        self.raw_config_content = raw_config_content

        # parse raw YAML content into a dictionary
        self.__parse_raw_config()

        # parse that dictionary into respective parts of prompt config
        self.__parse()

    # raw prompt template file
    def load_from_template_contents(self, raw_template_content):
        self.__parse_prompt_template_simple(raw_template_content)

    # raw prompt template file from file
    def load_from_template_contents_at_path(self, path):
        try:
            with open(path, "r") as file:
                return self.__parse_prompt_template_simple(file.read())

        except FileNotFoundError:
            print("The specified file does not exist.")

        except PermissionError:
            print("You do not have permission to access the specified file.")

        except Exception as e:
            print("An error occurred while opening the file:", str(e))

    # list keys/names of all services that we have configured in the config file
    def configured_services(self):
        return list(self.services.keys())

    def service_with_name(self, service_name):
        service_config = self.services.get(service_name)

        if service_config:
            return service_config
        else:
            return ServiceConfig(service_name, service_name)

    # returns options for specific service, already includes all option inheritance
    def options_for_service(self, service_name):
        return self.service_with_name(service_name).options

    def option_for_service(self, service_name, option_name):
        return self.options_for_service(service_name).value(option_name)

    def file_dependencies(self):
        if self.template:
            return self.template.file_dependencies()

        return []

    ####################################################

    def __parse(self):
        self.__parse_version()
        self.__parse_prompt()
        self.__parse_services()

    def __parse_raw_config(self):
        try:
            self.config_content = yaml.safe_load(self.raw_config_content)
        except yaml.YAMLError as exc:
            print(exc)

    def __parse_version(self):
        if self.config_content:
            self.version = self.config_content.get("version")

    def __parse_prompt_template_simple(self, content):
        self.template = PromptTemplateSimple(content, self.search_path)

    # high level "prompt:" parsing
    def __parse_prompt(self):
        if self.config_content:
            prompt = self.config_content.get("prompt")

            if prompt:
                content_file = prompt.get("content_file")
                content = prompt.get("content")
                messages = prompt.get("messages")

                if content_file:
                    include_contents = "{% include '" + content_file + "' %}"
                    self.template = PromptTemplateSimple(
                        include_contents, self.search_path
                    )
                elif content:
                    self.template = PromptTemplateSimple(content, self.search_path)
                elif messages:
                    self.template = PromptTemplateMessages(messages, self.search_path)

    # high level "services:" parsing
    def __parse_services(self):
        if self.config_content:
            _services = self.config_content.get("services")

            if _services:
                options_for_all_services = _services.get("options") or {}

                #
                # if we have models + prompt-level model options
                #
                # services:
                #   models:
                #     - 'openai/chat/gpt-4'
                #     - 'anthropic/complete/claude-v1.3-100k'
                #   options:
                #     max_tokens: 1337
                _models = _services.get("models")
                if _models:
                    for _model_name in _models:
                        service_config = ServiceConfig(
                            _model_name, _model_name, options_for_all_services
                        )

                        self.services[_model_name] = service_config

                else:
                    #
                    # if we have services defined with options for each
                    #
                    # services:
                    #   mygpt4:
                    #     model: 'openai/chat/gpt-4'
                    #     options:
                    #       temperature: 0.2
                    #       max_tokens: 4000
                    #   options:
                    #     max_tokens: 1337
                    for _service_name in _services:
                        if _service_name not in ["options", "models"]:
                            service = _services[_service_name]

                            # start with options for all services
                            # defined on a higher level
                            options = options_for_all_services.copy()

                            # update with service-level options
                            service_level_options = service.get("options")

                            if service_level_options:
                                options.update(service_level_options)

                            model = service.get("model")

                            service_config = ServiceConfig(
                                _service_name, model, options
                            )

                            self.services[_service_name] = service_config
