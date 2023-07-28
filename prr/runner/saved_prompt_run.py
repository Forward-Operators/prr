import os

from prr.runner.saved_service_run import SavedServiceRun


class SavedPromptRun:
    def __init__(self, run_subdir):
        self.run_subdir = run_subdir

        self.read_id()
        self.read_state()
        self.read_service_runs()

    def in_progress_file_path(self):
        return os.path.join(self.run_subdir, ".in-progress")

    def mark_as_in_progress(self):
        if not os.path.exists(self.run_subdir):
            os.makedirs(self.run_subdir)

        open(self.in_progress_file_path(), "a").close()

    def mark_as_done(self):
        in_progress_file = self.in_progress_file_path()

        if os.path.exists(in_progress_file):
            os.remove(in_progress_file)

    def read_state(self):
        self.state = "done"

        if os.path.exists(self.run_subdir + "/.in-progress"):
            self.state = "in-progress"

    def read_service_runs(self):
        self.service_runs = []

        if os.path.exists(self.run_subdir):
            service_subdirs = sorted(os.listdir(self.run_subdir))
            for service_subdir in service_subdirs:
                # ignore .in-progress and similar files
                if service_subdir.startswith("."):
                    continue

                self.service_runs.append(
                    SavedServiceRun(os.path.join(self.run_subdir, service_subdir))
                )

    def read_id(self):
        self.id = os.path.basename(self.run_subdir)

    def service_run(self, service_name):
        for run in self.service_runs:
            if run.name() == service_name:
                return run

    def service_run_names(self):
        all_service_run_names = []

        for run in self.service_runs:
            # only append if not already there
            if run.name() not in all_service_run_names:
                all_service_run_names.append(run.name())

        return all_service_run_names

    def last_service_run(self):
        if len(self.service_runs) == 0:
            return None

        return self.service_runs[-1]

    def save_service_run(self, service_name, result):
        run_directory = os.path.join(self.run_subdir, service_name.replace("/", "-"))

        new_saved_service_run = SavedServiceRun(run_directory)
        new_saved_service_run.save(result)

        return run_directory
