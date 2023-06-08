import os
import sys
import json
import hashlib
import threading
import webbrowser

from rich import print
from rich.console import Console
from rich.panel import Panel

from fastapi import FastAPI, Request, APIRouter, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import uvicorn

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from prr.runner.saved_run import SavedRunsCollection
from prr.runner import Runner
from prr.prompt.prompt_loader import PromptConfigLoader
from prr.ui.prompt_files import PromptFiles

console = Console(log_time=True, log_path=False)

def run_prompt():
  loader = PromptConfigLoader()
  prompt_config = loader.load_from_path(prompt_path())

  runner = Runner(prompt_config)

  console.log(
      "Running prompt:  "
      + "[green]"
      + prompt_path()
      + "[/green]"
  )

  runner.run_all_configured_services({}, True)

  console.log(
      "✅ Done running prompt: "
      + "[green]"
      + prompt_path()
      + "[/green]"
  )



def prompt_path():
  return os.environ["__PRR_WEB_UI_PROMPT_PATH"]

def collection():
  return SavedRunsCollection(prompt_path())

def render_args_for_run(run, service):
  if run.state == 'done' and service:
    return {
      "run_id": str(run.id()), 
      "service_name": service.name(), 
      "service": service,
      "prompt_content": service.prompt_content(),
      "output_content": service.output_content(),
      "run_details": service.run_details(),
      "prompt_file": os.path.basename(prompt_path()),
      "state": run.state,
      "prompt_name": os.path.basename(prompt_path())
    }

  return {
    "run_id": str(run.id()), 
    "state": run.state,
  }

def render_args(action, request, run, service, run2=None, service2=None):
    all_runs = sorted(collection().all(), key=lambda run: int(run.id()), reverse=True)

    all_service_names = [_service.name() for _service in run.services()]

    _args = {
      "action": action,
      "request": request,
      "primary": render_args_for_run(run, service),
      "secondary": False,
      "all_runs": all_runs,
      "all_service_names": all_service_names,
      "prompt_name": os.path.basename(prompt_path()),
    }

    if run2 and service2:
      _args["secondary"] = render_args_for_run(run2, service2)

    return _args

def service_from_run(run, service_name):
    if not service_name:
      _services = run.services()

      if len(_services) == 0:
        return None

      return run.services()[0]

    return run.service(service_name)

def run_from_collection(run_id):
    if run_id == None:
      return collection().latest()

    return collection().run(run_id)

def render_run(request, run_id=None, service_name=None):
    if collection().is_empty():
      args = { "request": request }
      return templates.TemplateResponse("no-runs-yet.html", args)

    run = run_from_collection(run_id)
    service = service_from_run(run, service_name)

    args = render_args('run', request, run, service)

    return templates.TemplateResponse("run.html", args)

def render_edit(request, file_id=None):
    prompt_files = PromptFiles(prompt_path())

    current_file_id = file_id

    if current_file_id == None:
      current_file_id = hashlib.md5(prompt_path().encode()).hexdigest()

    current_file_path = prompt_files.get_file_path(current_file_id)
    file_content = prompt_files.get_file_contents(current_file_id)

    args = {
      "action": "edit",
      "request": request,
      "files": prompt_files.files,
      "current_file_id": current_file_id,
      "file_content": file_content,
      "all_runs": collection().all(),
      "prompt_name": os.path.basename(prompt_path()),
    }

    return templates.TemplateResponse("edit.html", args)

def render_state(request):
    all_runs = collection().all()

    runs = []

    for run in all_runs:
      runs.append({ 'run_id': run.id(), 'state': run.state })

    return Response(json.dumps({ 'all_runs': runs }), media_type='application/json')

def render_update(request, data, file_id=None):

    prompt_files = PromptFiles(prompt_path())

    content = data['content']

    prompt_files.update_file(file_id, content)

    return Response('lol', media_type='text/plain')

def render_diff(request, run_id=None, service_name=None, run_id2=None, service_name2=None):
    run = run_from_collection(run_id)
    service = service_from_run(run, service_name)

    if run_id2 == None:
      run2 = collection().the_one_before(run.id())
    else:
      run2 = run_from_collection(run_id2)

    if run2:
      run_id2 = run2.id()

    if service_name2 == None:
      service_name2 = run2.services()[0].name()

    service2 = service_from_run(run2, service_name2)
    
    args = render_args('diff', request, run, service, run2, service2)

    return templates.TemplateResponse("diff.html", args)


app = FastAPI()
templates = Jinja2Templates(directory=(os.path.dirname(__file__) + "/templates"))

static_files_directory_path = os.path.dirname(__file__) + "/static"
app.mount("/static", StaticFiles(directory=static_files_directory_path), name="static")

@app.on_event("startup")
async def startup_event():
    webbrowser.open('http://localhost:8400/edit', new=2)

@app.get("/", response_class=RedirectResponse)
async def root(request: Request):
    return RedirectResponse("/runs", status_code=302)

@app.post("/run", response_class=RedirectResponse)
async def trigger_run(request: Request):
    thread = threading.Thread(target=run_prompt)
    thread.start()
    
    return RedirectResponse("/runs", status_code=302)

@app.get("/runs", response_class=HTMLResponse)
async def get_latest_run(request: Request):
    return render_run(request)

@app.get("/runs/{run_id}/{service_name}", response_class=HTMLResponse)
async def get_run(request: Request, run_id: str, service_name: str):
    return render_run(request, run_id, service_name)

@app.get("/state", response_class=Response)
async def get_runs_state(request: Request):
    return render_state(request)

@app.get("/edit", response_class=HTMLResponse)
async def edit_index(request: Request):
    return render_edit(request)

@app.get("/edit/{file_id}", response_class=HTMLResponse)
async def edit(request: Request, file_id: str):
    return render_edit(request, file_id)

@app.post("/edit/{file_id}", response_class=HTMLResponse)
async def update(request: Request, file_id: str):
    data = await request.json()
    return render_update(request, data, file_id)

@app.get("/compare", response_class=HTMLResponse)
async def compare_latest(request: Request):
    return render_diff(request)

@app.get("/compare/{run_id}/{service_name}", response_class=HTMLResponse)
async def compare_with_latest_run(request: Request, run_id: str, service_name: str):
    return render_diff(request, run_id, service_name)

@app.get("/compare/{run_id}/{service_name}/{run_id2}/{service_name2}", response_class=HTMLResponse)
async def compare(request: Request, run_id: str, service_name: str, run_id2: str, service_name2: str):
    return render_diff(request, run_id, service_name, run_id2, service_name2)
