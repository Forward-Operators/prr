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

def render_run(id, request, collection, service_name=None):
    run = collection.run(id)

    if not service_name:
      service = run.services()[0]
    else:
      service = run.service(service_name)

    all_run_ids = [_run.id() for _run in collection.all()]
    all_service_names = [_service.name() for _service in run.services()]

    args = {
      "request": request, 
      "id": str(id), 
      "service_name": service_name, 
      "service": service,
      "prompt_content": service.prompt_content(),
      "output_content": service.prompt_content(),
      "run_details": service.run_details(),
      "all_run_ids": sorted(all_run_ids, key=int, reverse=True),
      "all_service_names": all_service_names,
      "prompt_file": "chihuahua.yaml"
    }

    return templates.TemplateResponse("run.html", args)

@app.get("/", response_class=RedirectResponse)
async def root(request: Request):
    return RedirectResponse("/runs/latest", status_code=302)

@app.get("/runs/latest", response_class=HTMLResponse)
async def get_latest_run(request: Request):
    collection = SavedRunsCollection("/workspaces/prr/examples/configured/chihuahua.yaml")    
    id = collection.latest().id()
    service = collection.latest().services()[0]

    return render_run(id, request, collection, service.name())

@app.get("/runs/{_id}/{service_name}", response_class=HTMLResponse)
async def get_run(request: Request, _id: str, service_name: str):
    collection = SavedRunsCollection("/workspaces/prr/examples/configured/chihuahua.yaml")

    if _id == "latest":
      id = collection.latest().id()
    else:
      id = _id
    
    return render_run(id, request, collection, service_name)
