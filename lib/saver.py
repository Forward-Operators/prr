import os
from datetime import datetime

import yaml


class PromptRunSaver:
    def __init__(self, prompt):
        self.prompt_path = prompt.path
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
        dirname = os.path.dirname(self.prompt_path)
        basename = os.path.basename(self.prompt_path)

        root, extension = os.path.splitext(basename)

        if extension == ".yaml":
            basename = root

        runs_dir = os.path.join(dirname, f"{basename}.runs")

        return self.run_root_directory_path_for_runs_dir(runs_dir)

    def run_directory_path(self, model_or_model_config_name):
        model_name_part = model_or_model_config_name.replace("/", "-")

        return os.path.join(self.runs_subdir, model_name_part)

    def prepare_run_directory(self, model_or_model_config_name):
        run_dir = self.run_directory_path(model_or_model_config_name)

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

        with open(completion_file, "w") as f:
            f.write(response.response_content)

    def save_run(self, run_directory, result):
        run_file = os.path.join(run_directory, f"run.yaml")
        run_data = result.metrics()

        with open(run_file, "w") as f:
            yaml.dump(run_data, f, default_flow_style=False)

    def save(self, model_or_model_config_name, result):
        run_directory = self.prepare_run_directory(model_or_model_config_name)

        self.save_prompt(run_directory, result.request)
        self.save_completion(run_directory, result.response)
        self.save_run(run_directory, result)

        return run_directory
