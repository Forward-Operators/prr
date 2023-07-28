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

    def save_prompt(self, request):
        prompt_content = request.prompt_content

        if prompt_content:
            if isinstance(prompt_content, str):
                prompt_file = os.path.join(self.saved_service_run_path, f"prompt")

                with open(prompt_file, "w") as f:
                    f.write(prompt_content)
            else:
                prompt_file = os.path.join(self.saved_service_run_path, f"prompt.yaml")

                with open(prompt_file, "w") as f:
                    yaml.dump(prompt_content, f, default_flow_style=False)

    def save_completion(self, response):
        completion_file = os.path.join(self.saved_service_run_path, f"output")

        with open(completion_file, "w") as f:
            f.write(response.response_content)

    def save_run(self, result):
        run_file = os.path.join(self.saved_service_run_path, f"run.yaml")
        run_data = result.metrics()

        with open(run_file, "w") as f:
            yaml.dump(run_data, f, default_flow_style=False)

    def save(self, result):
        if not os.path.exists(self.saved_service_run_path):
            os.makedirs(self.saved_service_run_path)

        self.save_prompt(result.request)
        self.save_completion(result.response)
        self.save_run(result)
