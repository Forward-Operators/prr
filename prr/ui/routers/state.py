import json
import os

from fastapi import APIRouter, Request
from fastapi.responses import Response

from prr.prompt.prompt_loader import PromptConfigLoader
from prr.runner.run_collection import PromptRunCollection

state_router = APIRouter()


class StateRenderer:
    def __init__(self, prompt_path):
        self.prompt_path = prompt_path

        loader = PromptConfigLoader()
        prompt_config = loader.load_from_path(self.prompt_path)

        self.collection = PromptRunCollection(prompt_config)

    def state_for_run(self, run):
        return {
            "id": run.id,
            "state": run.state,
        }

    def render(self, request):
        runs = [self.state_for_run(run) for run in self.collection.runs]
        data = json.dumps({"all_runs": runs})
        return Response(data, media_type="application/json")


@state_router.get("/state", response_class=Response)
async def get_runs_state(request: Request):
    renderer = StateRenderer(os.environ["__PRR_WEB_UI_PROMPT_PATH"])
    return renderer.render(request)
