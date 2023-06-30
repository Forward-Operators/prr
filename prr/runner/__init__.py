from prr.runner.prompt_run import PromptRun
from prr.runner.run_collection import PromptRunCollection
from prr.services.service_registry import ServiceRegistry

service_registry = ServiceRegistry()
service_registry.register_all_services()


# high-level class to run prompts based on configuration
class Runner:
    def __init__(self, prompt_config, save_runs=False, prompt_args={}):
        self.prompt_config = prompt_config
        self.prompt_args = prompt_args
        self.current_run = None
        self.save_runs = save_runs

        if self.prompt_config.template == None:
            raise Exception("PromptConfig must have a template")

        self.run_collection = PromptRunCollection(self.prompt_config)

    def prepare_service_run(self, service_name, service_options_overrides):
        service_config = self.prompt_config.service_with_name(service_name)

        service_config.process_option_overrides(service_options_overrides)

        service = service_registry.service_for_service_config(service_config)

        self.current_run = PromptRun(
            self.prompt_config, self.prompt_args, service, service_config
        )

    def run_service(self, service_name):
        run_save_directory = None

        if self.save_runs == None:
            self.current_run_in_collection = self.run_collection.start_new_run()

        result = self.current_run.run()

        if self.save_runs:
            run_save_directory = self.run_collection.save_current_service_run(
                service_name, result
            )

        self.current_run = None

        return result, run_save_directory

    def current_run_request(self):
        return self.current_run.service.request

    def current_run_request_options(self):
        return self.current_run_request().options

    # runs all models defined for specified prompt
    def run_all_configured_services(self, service_options_overrides):
        self.run_services(
            self.prompt_config.configured_services(), service_options_overrides
        )

    def run_services(
        self,
        services,
        service_options_overrides={},
        callbacks={
            "on_request": lambda service_name, request: None,
            "on_result": lambda service_name, result, run_save_directory: None,
        },
    ):
        if self.save_runs:
            self.run_collection.start_new_run()

        for service_name in services:
            self.prepare_service_run(service_name, service_options_overrides)
            request = self.current_run_request()

            if callbacks["on_request"]:
                callbacks["on_request"](service_name, request)

            result, save_directory = self.run_service(service_name)

            if callbacks["on_result"]:
                callbacks["on_result"](service_name, result, save_directory)

        if self.save_runs:
            self.run_collection.finish_current_run()
