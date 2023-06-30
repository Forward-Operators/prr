import os
from datetime import datetime

from prr.runner.saved_prompt_run import SavedPromptRun


class PromptRunCollection:
    def __init__(self, prompt_config):
        self.prompt_config = prompt_config
        self.run_time = datetime.now()
        self.dot_runs_dir = self.dot_runs_path()
        self.current_run = None

        if not os.path.isdir(self.dot_runs_dir):
            self.runs = []
        else:
            self.read_runs()

    def start_new_run(self):
        self.current_run = SavedPromptRun(self.new_run_path(self.dot_runs_dir))
        self.current_run.mark_as_in_progress()

    def save_current_service_run(self, service_name, result):
        return self.current_run.save_service_run(service_name, result)

    def finish_current_run(self):
        self.current_run.mark_as_done()
        self.current_run = None

    def read_runs(self):
        if not os.path.isdir(self.dot_runs_dir):
            self.runs = []
        else:
            run_subdirs_unsorted = os.listdir(self.dot_runs_dir)
            run_subdirs = sorted(run_subdirs_unsorted, key=lambda x: int(x))
            self.runs = [
                SavedPromptRun(os.path.join(self.dot_runs_dir, run_dir))
                for run_dir in run_subdirs
            ]

    def is_empty(self):
        return self.runs == []

    def has_done_runs(self):
        done_runs = [run for run in self.runs if run.state == "done"]

        if len(done_runs) == 0:
            return False

        return True

    def latest_run(self):
        if len(self.runs) == 0:
            return None

        return self.runs[-1]

    def the_one_before(self, run_id):
        if int(run_id) == "1":
            return self.run(run_id)
        else:
            return self.run(str(int(run_id) - 1))

    def run(self, run_id):
        for run in self.runs:
            if run.id == run_id:
                return run

        return None

    def new_run_path(self, runs_dir):
        try:
            previous_runs = os.listdir(runs_dir)
        except FileNotFoundError:
            return os.path.join(runs_dir, "1")

        run_id = 1
        while True:
            run_dir = os.path.join(runs_dir, str(run_id))

            if not os.path.exists(run_dir):
                return run_dir

            run_id += 1

    def dot_runs_path(self):
        dirname = self.prompt_config.search_path

        if self.prompt_config.filename:
            basename = os.path.basename(self.prompt_config.filename)
        else:
            basename = "prr"

        root, extension = os.path.splitext(basename)

        if extension == ".yaml":
            basename = root

        return os.path.join(dirname, f"{basename}.runs")

    def run_directory_path(self, service_or_model_name):
        model_name_part = service_or_model_name.replace("/", "-")

        return os.path.join(self.dot_runs_dir, model_name_part)

    def prepare_run_directory(self, service_or_model_name):
        run_dir = self.run_directory_path(service_or_model_name)

        os.makedirs(run_dir, exist_ok=True)

        return run_dir
