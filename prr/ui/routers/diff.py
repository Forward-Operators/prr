import os

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from prr.prompt.prompt_loader import PromptConfigLoader
from prr.runner.run_collection import PromptRunCollection

diff_router = APIRouter()

templates = Jinja2Templates(directory=(os.path.dirname(__file__) + "/../templates"))


class DiffRenderer:
    def __init__(self, prompt_path):
        self.prompt_path = prompt_path

        loader = PromptConfigLoader()
        self.prompt_config = loader.load_from_path(self.prompt_path)

        self.collection = PromptRunCollection(self.prompt_config)

    def process_arguments(self, run_id, service_name, run_id2, service_name2):
        if run_id == None:
            run = self.collection.latest_run()
        else:
            run = self.collection.run(run_id)

        if service_name == None:
            service = run.last_service_run()
        else:
            service = run.service_run(service_name)

        if run_id2 == None:
            run2 = self.collection.the_one_before(run.id)
        else:
            run2 = self.collection.run(run_id2)

        if run2:
            if service_name2 == None:
                service2 = run2.last_service_run()
            else:
                service2 = run2.service_run(service_name2)

                if service2 == None:
                    service2 = run2.last_service_run()
        else:
            run2 = run
            service2 = service

        return run, service, run2, service2

    def diff(
        self, request, run_id=None, service_name=None, run_id2=None, service_name2=None
    ):
        if self.collection.is_empty():
            message = f"No runs for {self.prompt_name()} yet"
            template_args = {
                "request": request,
                "page_title": message,
                "error_message": message,
            }

            return templates.TemplateResponse("error.html", template_args)

        run, service, run2, service2 = self.process_arguments(
            run_id, service_name, run_id2, service_name2
        )

        template_args = self.render_template_args(request, run, service, run2, service2)

        return templates.TemplateResponse("diff.html", template_args)

    def run_template_args(self, run, service):
        if run.state == "done" and service:
            return {
                "run_id": str(run.id),
                "service_name": service.name(),
                "service": service,
                "prompt_content": service.prompt_content(),
                "output_content": service.output_content(),
                "run_details": service.run_details(),
                "state": run.state,
            }

        return {
            "run_id": str(run.id),
            "state": run.state,
        }

    def prompt_name(self):
        return os.path.basename(self.prompt_path)

    def all_runs_sorted(self):
        return sorted(self.collection.runs, key=lambda run: int(run.id), reverse=True)

    def request_option_keys_for_services(self, services):
        option_keys = []

        for service in services:
            if service != None:
                option_keys += service.run_details()["request"]["options"].keys()

        return sorted(set(option_keys))

    def response_keys_for_services(self, services):
        response_keys = []

        for service in services:
            if service != None:
                response_keys += service.run_details()["response"].keys()

        return sorted(set(response_keys))

    def render_template_args(self, request, run, service, run2, service2):
        all_runs = self.all_runs_sorted()
        all_service_names = run.service_run_names()

        requests_option_keys = self.request_option_keys_for_services(
            [service, service2]
        )
        response_keys = self.response_keys_for_services([service, service2])

        return {
            "action": "diff",
            "request": request,
            "run": self.run_template_args(run, service),
            "run2": self.run_template_args(run2, service2),
            "all_runs": all_runs,
            "all_service_names": all_service_names,
            "prompt_name": self.prompt_name(),
            "prompt_file": self.prompt_path,
            "requests_option_keys": requests_option_keys,
            "response_keys": response_keys,
            "page_title": f"{self.prompt_name()}: #{run.id}/{service.name()} vs #{run2.id}/{service2.name()}",
        }


def renderer():
    return DiffRenderer(os.environ["__PRR_WEB_UI_PROMPT_PATH"])


@diff_router.get("/diff", response_class=HTMLResponse)
async def diff_latest(request: Request):
    return renderer().diff(request)


@diff_router.get("/diff/{run_id}/{service_name}", response_class=HTMLResponse)
async def diff_with_latest_run(request: Request, run_id: str, service_name: str):
    return renderer().diff(request, run_id, service_name)


@diff_router.get(
    "/diff/{run_id}/{service_name}/{run_id2}/{service_name2}",
    response_class=HTMLResponse,
)
async def diff(
    request: Request, run_id: str, service_name: str, run_id2: str, service_name2: str
):
    return renderer().diff(request, run_id, service_name, run_id2, service_name2)
