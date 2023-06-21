import os
import sys
import json
import hashlib
import threading
import webbrowser


from fastapi import FastAPI, Request, APIRouter, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import uvicorn

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from prr.runner import Runner
from prr.prompt.prompt_loader import PromptConfigLoader

from prr.ui.routers.runs import runs_router
from prr.ui.routers.state import state_router
from prr.ui.routers.edit import edit_router


def render_diff(request, run_id=None, service_name=None, run_id2=None, service_name2=None):
    run = run_from_collection(run_id)
    service = service_from_run(run, service_name)

    if run_id2 == None:
      run2 = collection().the_one_before(run.id)
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

app.include_router(runs_router)
app.include_router(state_router)
app.include_router(edit_router)

@app.on_event("startup")
async def startup_event():
    webbrowser.open('http://localhost:8400/', new=2)

@app.get("/", response_class=RedirectResponse)
async def root(request: Request):
    return RedirectResponse("/edit", status_code=302)


@app.get("/compare", response_class=HTMLResponse)
async def compare_latest(request: Request):
    return render_diff(request)

@app.get("/compare/{run_id}/{service_name}", response_class=HTMLResponse)
async def compare_with_latest_run(request: Request, run_id: str, service_name: str):
    return render_diff(request, run_id, service_name)

@app.get("/compare/{run_id}/{service_name}/{run_id2}/{service_name2}", response_class=HTMLResponse)
async def compare(request: Request, run_id: str, service_name: str, run_id2: str, service_name2: str):
    return render_diff(request, run_id, service_name, run_id2, service_name2)
