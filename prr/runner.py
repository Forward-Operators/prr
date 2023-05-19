from .prompt_run import PromptRun
from .saver import PromptRunSaver
from .service_registry import ServiceRegistry

service_registry = ServiceRegistry()
service_registry.register_all_services()

# high-level class to run prompts based on configuration
class Runner:
    def __init__(self, prompt_config):
        self.prompt_config = prompt_config
        self.saver = PromptRunSaver(self.prompt_config)

    def run_service(self, service_name, service_options_overrides, save_run=False):
        service_config = self.prompt_config.service_with_name(service_name)

        service_config.process_option_overrides(service_options_overrides)

        service = service_registry.service_for_service_config(service_config)

        result = PromptRun(self.prompt_config, service, service_config).run()

        if save_run:
            run_save_directory = self.saver.save(service_name, result)
        else:
            run_save_directory = None

        return result, run_save_directory

    # runs all models defined for specified prompt
    def run_all_configured_services(self, service_options_overrides, save_run=False):
        results = {}

        for service_name in self.configured_services():
            results[service_name] = self.run_service(service_name, service_options_overrides, save_run)

        return results
