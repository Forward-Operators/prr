import os
import sys

from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import uvicorn

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from prr.runner.saved_run import SavedRunsCollection

def collection():
  return SavedRunsCollection(os.environ["__PRR_WEB_UI_PROMPT_PATH"])

def render_args_for_run(run, service):
  return {
    "run_id": str(run.id()), 
    "service_name": service.name(), 
    "service": service,
    "prompt_content": service.prompt_content(),
    "output_content": service.output_content(),
    "run_details": service.run_details(),
    "prompt_file": os.path.basename(os.environ["__PRR_WEB_UI_PROMPT_PATH"])
  }

def render_args(request, run, service, run2=None, service2=None):
    all_run_ids = [_run.id() for _run in collection().all()]
    all_service_names = [_service.name() for _service in run.services()]

    _args = {
      "request": request,
      "primary": render_args_for_run(run, service),
      "secondary": False,
      "all_run_ids": sorted(all_run_ids, key=int, reverse=True),
      "all_service_names": all_service_names,
    }

    if run2 and service2:
      _args["secondary"] = render_args_for_run(run2, service2)

    return _args

def service_from_run(run, service_name):
    if not service_name:
      return run.services()[0]

    return run.service(service_name)

def run_from_collection(run_id):
    if run_id == "latest" or run_id == None:
      return collection().latest()

    return collection().run(run_id)

def render_run(request, run_id=None, service_name=None):
    run = run_from_collection(run_id)
    service = service_from_run(run, service_name)

    args = render_args(request, run, service)

    return templates.TemplateResponse("run.html", args)

def render_diff(request, run_id=None, service_name=None, run_id2=None, service_name2=None):
    run = run_from_collection(run_id)
    service = service_from_run(run, service_name)

    if run_id2 == None:
      run2 = collection().latest_minus_one()
    else:
      run2 = run_from_collection(run_id2)

    if run2:
      run_id2 = run2.id()

    if service_name2 == None:
      service_name2 = run2.services()[0].name()

    service2 = service_from_run(run2, service_name2)
    
    args = render_args(request, run, service, run2, service2)

    return templates.TemplateResponse("diff.html", args)


app = FastAPI()
templates = Jinja2Templates(directory=(os.path.dirname(__file__) + "/templates"))

static_files_directory_path = os.path.dirname(__file__) + "/static"
app.mount("/static", StaticFiles(directory=static_files_directory_path), name="static")

@app.get("/", response_class=RedirectResponse)
async def root(request: Request):
    return RedirectResponse("/runs/latest", status_code=302)

@app.get("/runs/latest", response_class=HTMLResponse)
async def get_latest_run(request: Request):
    return render_run(request)

@app.get("/runs/{run_id}/{service_name}", response_class=HTMLResponse)
async def get_run(request: Request, run_id: str, service_name: str):
    return render_run(request, run_id, service_name)

@app.get("/compare/{run_id}/{service_name}", response_class=HTMLResponse)
async def compare_latest(request: Request, run_id: str, service_name: str):
    return render_diff(request, run_id, service_name)

@app.get("/compare/{run_id}/{service_name}/{run_id2}/{service_name2}", response_class=HTMLResponse)
async def compare(request: Request, run_id: str, service_name: str, run_id2: str, service_name2: str):
    return render_diff(request, run_id, service_name, run_id2, service_name2)
