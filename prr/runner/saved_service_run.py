import os
import yaml

class SavedServiceRun:
  def __init__(self, saved_service_run_path):
    self.saved_service_run_path = saved_service_run_path

  def name(self):
    return os.path.basename(self.saved_service_run_path)

  def prompt_content(self):
    return self.read_file(["prompt.yaml", "prompt"])

  def read_file(self, filenames):
    for filename in filenames:
      filename_path = os.path.join(self.saved_service_run_path, filename)

      if os.path.isfile(filename_path) and os.access(filename_path, os.R_OK):
        return open(filename_path, "r").read()

  def output_content(self):
    # "completion" is old style
    return self.read_file(["output", "completion"])

  def run_details(self):
    #  try-catch on yaml load here
    content = self.run_details_content()

    if content:
      yaml_content = yaml.safe_load(content)
      return yaml_content

    return {}

  def run_details_content(self):
    return self.read_file(["run.yaml"])