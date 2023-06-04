import os
import sys

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from prr.runner.saved_run import SavedRunsCollection

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    collection = SavedRunsCollection("/workspaces/prr/examples/configured/chihuahua.yaml")
    runs = collection.all()

    available_run_ids = [run.id() for run in runs]

    return templates.TemplateResponse("runs.html", {
      'request': request,
      'available_run_ids': available_run_ids
    })


@app.get("/runs/{id}/{service_name}", response_class=HTMLResponse)
async def get_run(request: Request, id: int, service_name: str):
    collection = SavedRunsCollection("/workspaces/prr/examples/configured/chihuahua.yaml")
    run = collection.run(id)
    service = run.service(service_name)

    args = {
      "request": request, 
      "id": str(id), 
      "service_name": service_name, 
      "service": service,
      "prompt_content": service.prompt_content(),
      "output_content": service.prompt_content(),
      "run_details": service.run_details(),
    }

    return templates.TemplateResponse("run.html", args)


@app.get("/runs/{id}", response_class=HTMLResponse)
async def get_services(request: Request, id: int):
    collection = SavedRunsCollection("/workspaces/prr/examples/configured/chihuahua.yaml")
    run = collection.run(id)
    service_names = [service.name() for service in run.services()]

    args = {"request": request, "id": str(id), "services": service_names}
    return templates.TemplateResponse("services.html", args)
