import os

import jinja2
from jinja2 import meta


class PromptMessage:
    def __init__(
        self, content_template_string, search_path=".", role="user", name=None
    ):
        self.content_template_string = content_template_string
        self.search_path = search_path
        self.role = role
        self.name = name
        self.file_dependencies = []

        template_loader = jinja2.ChoiceLoader(
            [
                jinja2.FileSystemLoader(search_path),
                jinja2.FileSystemLoader(["/"]),
            ]
        )

        self.template_env = jinja2.Environment(loader=template_loader)
        self.__add_dependency_files_from_jinja_template(content_template_string)

        self.template = self.template_env.from_string(self.content_template_string)

    def is_system(self):
        return self.role == "system"

    def is_user(self):
        return self.role == "user"

    def is_assistant(self):
        return self.role == "assistant"

    def render_text(self, prompt_args=None):
        return self.template.render({"prompt_args": prompt_args})

    def render_message(self, prompt_args=None):
        _message = {"role": self.role, "content": self.render_text(prompt_args)}

        if self.name:
            _message.update({"name": self.name})

        return _message

    def __add_dependency_files_from_jinja_template(self, jinja_template_content):
        parsed_content = self.template_env.parse(jinja_template_content)
        referenced_templates = jinja2.meta.find_referenced_templates(parsed_content)

        self.file_dependencies.extend(referenced_templates)


# base class
class PromptTemplate:
    def __init__(self):
        self.messages = []

    def render_text(self, args=None):
        rendered_texts = [message.render_text(args) for message in self.messages]

        return "\n".join(rendered_texts)

    def render_messages(self, args=None):
        return [message.render_message(args) for message in self.messages]

    def file_dependencies(self):
        _dependencies = []
        for message in self.messages:
            for dependency in message.file_dependencies:
                if dependency not in _dependencies:
                    _dependencies.append(dependency)

        return _dependencies


# just a text/template file or prompt.contents from config
class PromptTemplateSimple(PromptTemplate):
    def __init__(self, template_string, search_path="."):
        self.messages = [PromptMessage(template_string, search_path, "user")]


# prompt.messages: key from config
class PromptTemplateMessages(PromptTemplate):
    # 'messages' are passed here verbatim after parsing YAML
    def __init__(self, messages, search_path="."):
        super().__init__()

        for message in messages:
            prompt_message = None

            role = message.get("role")
            name = message.get("name")
            content = message.get("content")
            content_file = message.get("content_file")

            if content:
                prompt_message = PromptMessage(content, search_path, role, name)
            elif content_file:
                include_contents = "{% include '" + content_file + "' %}"
                prompt_message = PromptMessage(
                    include_contents, search_path, role, name
                )

            if prompt_message:
                self.messages.append(prompt_message)
