from .prompt_run import PromptRun
from .saver import PromptRunSaver
from .service_registry import ServiceRegistry

service_registry = ServiceRegistry()
service_registry.register_all_services()


# high-level class to run prompts based on configuration
class Runner:
    def __init__(self, prompt):
        self.prompt = prompt
        self.saver = PromptRunSaver(self.prompt)

    def run_service(self, service_name, save_run=False):
        service_config = self.prompt.config_for_service(service_name)

        service = service_registry.service_for_service_config(service_config)

        result = PromptRun(self.prompt, service, service_config).run()

        if save_run:
            run_save_directory = self.saver.save(service_name, result)
        else:
            run_save_directory = None

        return result, run_save_directory

    # runs all models defined for specified prompt
    def run_all_configured_services(self):
        results = {}

        for model in self.configured_services():
            results[model] = self.run_service(model)

        return results
