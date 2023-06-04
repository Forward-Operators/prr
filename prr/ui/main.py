import os
import sys

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from prr.runner.saved_run import SavedRunsCollection

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# app.mount("/static", StaticFiles(directory="static"), name="static")

def render_args_for_run(run, service):
  return {
    "run_id": str(run.id()), 
    "service_name": service.name(), 
    "service": service,
    "prompt_content": service.prompt_content(),
    "output_content": service.output_content(),
    "run_details": service.run_details(),
    "prompt_file": "chihuahua.yaml"
  }

def render_args(request, collection, run, service, run2=None, service2=None):
    all_run_ids = [_run.id() for _run in collection.all()]
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

def run_from_collection(collection, run_id):
    if run_id == "latest" or run_id == None:
      return collection.latest()

    return collection.run(run_id)

def render_run(request, collection, run_id=None, service_name=None):
    run = run_from_collection(collection, run_id)
    service = service_from_run(run, service_name)

    args = render_args(request, collection, run, service)

    return templates.TemplateResponse("run.html", args)

def render_diff(request, collection, run_id=None, service_name=None, run_id2=None, service_name2=None):
    run = run_from_collection(collection, run_id)
    service = service_from_run(run, service_name)

    if run_id2 == None:
      run2 = collection.latest_minus_one()

      if run2:
        run_id2 = run2.id()

    if service_name2 == None:
      service_name2 = run2.services()[0].name()

    service2 = service_from_run(run2, service_name2)
    
    args = render_args(request, collection, run, service, run2, service2)

    return templates.TemplateResponse("run.html", args)

@app.get("/", response_class=RedirectResponse)
async def root(request: Request):
    return RedirectResponse("/runs/latest", status_code=302)

@app.get("/runs/latest", response_class=HTMLResponse)
async def get_latest_run(request: Request):
    collection = SavedRunsCollection("/workspaces/prr/examples/configured/chihuahua.yaml")    
    return render_run(request, collection)

@app.get("/runs/{run_id}/{service_name}", response_class=HTMLResponse)
async def get_run(request: Request, run_id: str, service_name: str):
    collection = SavedRunsCollection("/workspaces/prr/examples/configured/chihuahua.yaml")

    return render_run(request, collection, run_id, service_name)

@app.get("/compare/{run_id}/{service_name}", response_class=HTMLResponse)
async def compare_latest(request: Request, run_id: str, service_name: str):
    collection = SavedRunsCollection("/workspaces/prr/examples/configured/chihuahua.yaml")

    return render_diff(request, collection, run_id, service_name)

@app.get("/compare/{run_id}/{service_name}/{run_id2}/{service_name2}", response_class=HTMLResponse)
async def compare(request: Request, run_id: str, service_name: str, run_id2: str, service_name2: str):
    collection = SavedRunsCollection("/workspaces/prr/examples/configured/chihuahua.yaml")

    return render_diff(request, collection, run_id, service_name)
