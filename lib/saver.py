import os
import json
from datetime import datetime

class PromptRunSaver:
  def __init__(self):
    self.run_time = datetime.now()

  def run_time_str(self):
    return self.run_time.strftime("%Y-%m-%d_%H:%M:%S.%f")
  
  def prepare_run_directory(self, model_or_model_config_name, prompt_path):
    model_path_part = model_or_model_config_name.replace("/", "-")

    dirname = os.path.dirname(prompt_path)
    basename = os.path.basename(prompt_path)

    run_dir = os.path.join(dirname, f'{basename}.runs', self.run_time_str(), model_path_part)

    os.makedirs(run_dir, exist_ok=True)

    return run_dir
  
  def save_prompt(self, run_directory, prompt):
    prompt_file = os.path.join(run_directory, f"prompt.txt")

    with open(prompt_file, "w") as f:
      f.write(prompt.template)

  def save_config(self, run_directory, config):
    config_file = os.path.join(run_directory, f"config.json")

    with open(config_file, "w") as outfile:
      json.dump(config, outfile)

  def save_completion(self, run_directory, response):
    completion_file = os.path.join(run_directory, f"completion.txt")

    with open(completion_file, "w") as f:
      f.write(response.completion)

  def save_metrics(self, run_directory, result):
    metrics_file = os.path.join(run_directory, f"metrics.json")

    metrics = {
      'elapsed_time': result.elapsed_time,
      'tokens_used': result.response.tokens_used,
    }

    with open(metrics_file, "w") as f:
      json.dump(metrics, f)

  def save(self, model_or_model_config_name, result):
    run_directory = self.prepare_run_directory(model_or_model_config_name, result.prompt.path)

    self.save_prompt(run_directory, result.prompt)
    self.save_config(run_directory, result.config)
    self.save_completion(run_directory, result.response)
    self.save_metrics(run_directory, result)