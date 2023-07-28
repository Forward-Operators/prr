import os
import threading

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from prr.commands.run import RunPromptCommand
from prr.prompt.prompt_loader import PromptConfigLoader
from prr.runner import Runner
from prr.runner.run_collection import PromptRunCollection

runs_router = APIRouter()

templates = Jinja2Templates(directory=(os.path.dirname(__file__) + "/../templates"))


class RunRenderer:
    def __init__(self, prompt_path):
        self.prompt_path = prompt_path

        loader = PromptConfigLoader()
        self.prompt_config = loader.load_from_path(self.prompt_path)

        self.collection = PromptRunCollection(self.prompt_config)

    def trigger_run(self):
        args = {
            "command": "run",
            "abbrev": False,
            "quiet": False,
            "log": True,
            "prompt_path": self.prompt_path,
        }

        command = RunPromptCommand(args)
        command.run_prompt()

    def run(self, request, run_id=None, service_name=None):
        if self.collection.is_empty():
            message = f"No runs for {self.prompt_name()} yet"
            args = {
                "run": None,
                "run2": None,
                "request": request,
                "page_title": message,
                "error_message": message,
            }

            return templates.TemplateResponse("error.html", args)

        if run_id == None:
            run = self.collection.latest_run()
        else:
            run = self.collection.run(run_id)

        if service_name == None:
            service = run.last_service_run()
        else:
            service = run.service_run(service_name)

            if service == None:
                service = run.last_service_run()

        args = self.render_args("run", request, run, service)

        return templates.TemplateResponse("run.html", args)

    def run_args(self, run, service):
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

    def render_args(self, action, request, run, service):
        all_runs = sorted(
            self.collection.runs, key=lambda run: int(run.id), reverse=True
        )
        all_service_names = run.service_run_names()

        return {
            "action": action,
            "request": request,
            "run": self.run_args(run, service),
            "all_runs": all_runs,
            "all_service_names": all_service_names,
            "prompt_name": self.prompt_name(),
            "prompt_file": self.prompt_path,
            "page_title": f"{self.prompt_name()}/#{run.id}",
        }


def renderer():
    return RunRenderer(os.environ["__PRR_WEB_UI_PROMPT_PATH"])


@runs_router.post("/", response_class=RedirectResponse)
async def trigger_run(request: Request):
    _renderer = renderer()
    thread = threading.Thread(target=_renderer.trigger_run)
    thread.start()

    return RedirectResponse("/runs", status_code=302)


@runs_router.get("/runs", response_class=HTMLResponse)
async def get_latest_run(request: Request):
    return renderer().run(request)


@runs_router.get("/runs/{run_id}/{service_name}", response_class=HTMLResponse)
async def get_run(request: Request, run_id: str, service_name: str):
    return renderer().run(request, run_id, service_name)
