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
    print("------------ read_file(" + str(filenames) + ")")
    for filename in filenames:
      print("------------ " + filename)
      filename_path = os.path.join(self.saved_service_run_path, filename)
      print("------------ " + filename_path)

      if os.path.isfile(filename_path) and os.access(filename_path, os.R_OK):
        return open(filename_path, "r").read()

  def output_content(self):
    # "completion" is old style
    return self.read_file(["output", "completion"])

  def run_details(self):
    #  try-catch on yaml load here
    content = self.run_details_content()
    print ("CONTENT", content)

    if content:
      yaml_content = yaml.safe_load(content)
      print ("YAML CONTENT", yaml_content)
      return yaml_content

    return {}

  def run_details_content(self):
    print ("*** run_details_content")
    return self.read_file(["run.yaml"])




class SavedRun:
  def __init__(self, run_subdir_path):
    self.run_subdir_path = run_subdir_path

    self.state = 'done'

    if os.path.exists(self.run_subdir_path + '/.in-progress'):
      self.state = 'in-progress'

  def services(self):
    service_subdirs = []

    for subdir in os.listdir(self.run_subdir_path):
      if subdir.startswith('.'):
        continue

      service_subdirs.append(subdir)
      
    
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
    if not os.path.isdir(self.runs_directory_path):
      return []

    run_subdirs = os.listdir(self.runs_directory_path)

    run_subdirs = sorted(run_subdirs, key=lambda x: x.split('.')[0])

    return [SavedRun(os.path.join(self.runs_directory_path, run_subdir)) for run_subdir in run_subdirs]

  def is_empty(self):
    return len(self.all()) == 0


  def has_done_runs(self):
    _all = self.all()

    # filter our only runs that run.state == 'done'
    _all = [run for run in _all if run.state == 'done']

    if len(_all) == 0:
      return False

    return True
    

  def latest(self):
    _all = self.all()

    if len(_all) == 0:
      return None

    return self.all()[-1]

  def the_one_before(self, run_id):
    _all = self.all()

    if run_id == "1":
      return self.run(run_id)

    for i in range(len(_all)):
      if int(_all[i].id()) == int(run_id) -1:
        return _all[i]
    
    return None

  def run(self, run_id):
    return SavedRun(os.path.join(self.runs_directory_path, run_id))
