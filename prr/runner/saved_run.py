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
    return yaml.load(self.run_details_content(), Loader=yaml.FullLoader)

  def run_details_content(self):
    return self.read_file(["run.yaml"])




class SavedRun:
  def __init__(self, run_subdir_path):
    self.run_subdir_path = run_subdir_path

  def services(self):
    service_subdirs = os.listdir(self.run_subdir_path)
    return [SavedServiceRun(os.path.join(self.run_subdir_path, service_subdir)) for service_subdir in service_subdirs]

  def id(self):
    return os.path.basename(self.run_subdir_path)

  def service(self, service_name):
    service_subdir = os.path.join(self.run_subdir_path, service_name)
    return SavedServiceRun(service_subdir)


class SavedRunsCollection:
  def __init__(self, runs_directory_path):
    if runs_directory_path is None:
      raise ValueError("runs_directory_path cannot be None")

    if runs_directory_path.endswith('.yaml'):
      directory = os.path.dirname(runs_directory_path)
      base = os.path.basename(runs_directory_path)
      base_name, extension = os.path.splitext(base)
      runs_directory_path = os.path.join(directory, base_name)

    if runs_directory_path.endswith('.runs'):
      self.runs_directory_path = runs_directory_path
    else:
      self.runs_directory_path = runs_directory_path + '.runs'

  def all(self):
    run_subdirs = os.listdir(self.runs_directory_path)

    run_subdirs = sorted(run_subdirs, key=int)

    return [SavedRun(os.path.join(self.runs_directory_path, run_subdir)) for run_subdir in run_subdirs]

  def run(self, run_id):
    return SavedRun(os.path.join(self.runs_directory_path, str(int(run_id))))
