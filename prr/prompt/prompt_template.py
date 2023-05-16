import jinja2

class PromptTemplate:
  def __init__(self, template_string, search_path):
    template_loader = jinja2.FileSystemLoader(searchpath=search_path)
    self.template_env = jinja2.Environment(loader=template_loader)

    self.template_string = template_string
    self.template = self.template_env.from_string(template_string)

  def text(self, args=[]):
    return self.template.render({"prompt_args": args})
