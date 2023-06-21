import os
import yaml

from prr.runner.saved_service_run import SavedServiceRun

class SavedPromptRun:
  def __init__(self, run_subdir):
    self.run_subdir = run_subdir

    self.read_id()
    self.read_state()
    self.read_service_runs()

  def read_state(self):
    self.state = 'done'

    if os.path.exists(self.run_subdir + '/.in-progress'):
      self.state = 'in-progress'

  def read_service_runs(self):
    service_subdirs = []

    for service_subdir in os.listdir(self.run_subdir):
      if service_subdir.startswith('.'):
        continue

      service_subdirs.append(service_subdir)
      
    self.service_runs = [SavedServiceRun(os.path.join(self.run_subdir, service_subdir)) for service_subdir in service_subdirs]

  def read_id(self):
    self.id = os.path.basename(self.run_subdir)

  def service_run(self, service_name):
    for run in self.service_runs:
      if run.name() == service_name:
        return run
