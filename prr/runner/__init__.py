from prr.runner.prompt_run import PromptRun
from prr.runner.run_collection import PromptRunCollection
from prr.services.service_registry import ServiceRegistry

service_registry = ServiceRegistry()
service_registry.register_all_services()


# high-level class to run prompts based on configuration
class Runner:
    def __init__(self, prompt_config):
        self.prompt_config = prompt_config

        if self.prompt_config.template == None:
           raise Exception("PromptConfig must have a template")

        self.run_collection = PromptRunCollection(self.prompt_config)

    def run_service(self, service_name, service_options_overrides, save_run=False, single=True):
        if save_run and single:
          self.current_run_in_collection = self.run_collection.start_new_run()

        service_config = self.prompt_config.service_with_name(service_name)

        service_config.process_option_overrides(service_options_overrides)

        service = service_registry.service_for_service_config(service_config)

        result = PromptRun(self.prompt_config, service, service_config).run()

        if save_run:
            run_save_directory = self.run_collection.save_run(service_name, result)
        else:
            run_save_directory = None

        if save_run and single:
          self.run_collection.finish_current_run()

        return result, run_save_directory

    # runs all models defined for specified prompt
    def run_all_configured_services(self, service_options_overrides, save_run=False):
        results = {}

        if save_run:
          self.run_collection.start_new_run()

        for service_name in self.prompt_config.configured_services():
            results[service_name] = self.run_service(
                service_name, service_options_overrides, save_run, False
            )

        if save_run:
          self.run_collection.finish_current_run()

        return results
