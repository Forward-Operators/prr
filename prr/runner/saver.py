import os
from datetime import datetime

import yaml


class PromptRunSaver:
    def __init__(self, prompt_config):
        self.prompt_config = prompt_config
        self.run_time = datetime.now()
        self.runs_subdir = self.run_root_directory_path()

    def run_root_directory_path_for_runs_dir(self, runs_dir):
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

    def run_root_directory_path(self):
        dirname = self.prompt_config.search_path

        if self.prompt_config.filename:
            basename = os.path.basename(self.prompt_config.filename)
        else:
            basename = "prr"

        root, extension = os.path.splitext(basename)

        if extension == ".yaml":
            basename = root

        runs_dir = os.path.join(dirname, f"{basename}.runs")

        return self.run_root_directory_path_for_runs_dir(runs_dir)

    def run_directory_path(self, service_or_model_name):
        model_name_part = service_or_model_name.replace("/", "-")

        return os.path.join(self.runs_subdir, model_name_part)

    def prepare_run_directory(self, service_or_model_name):
        run_dir = self.run_directory_path(service_or_model_name)

        os.makedirs(run_dir, exist_ok=True)

        return run_dir

    def save_prompt(self, run_directory, request):
        prompt_content = request.prompt_content

        if prompt_content:
            if isinstance(prompt_content, str):
                prompt_file = os.path.join(run_directory, f"prompt")

                with open(prompt_file, "w") as f:
                    f.write(prompt_content)
            else:
                prompt_file = os.path.join(run_directory, f"prompt.yaml")

                with open(prompt_file, "w") as f:
                    yaml.dump(prompt_content, f, default_flow_style=False)

    def save_completion(self, run_directory, response):
        completion_file = os.path.join(run_directory, f"completion")

        fileoptions = "wb"

        if isinstance(response.response_content, str):
            fileoptions = "w"

        with open(completion_file, fileoptions) as f:
            f.write(response.response_content)

    def save_run(self, run_directory, result):
        run_file = os.path.join(run_directory, f"run.yaml")
        run_data = result.metrics()

        with open(run_file, "w") as f:
            yaml.dump(run_data, f, default_flow_style=False)

    def save(self, service_or_model_name, result):
        run_directory = self.prepare_run_directory(service_or_model_name)

        self.save_prompt(run_directory, result.request)
        self.save_completion(run_directory, result.response)
        self.save_run(run_directory, result)

        return run_directory
