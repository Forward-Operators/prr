import os
import sys
import webbrowser

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from prr.ui.routers.diff import diff_router
from prr.ui.routers.edit import edit_router
from prr.ui.routers.runs import runs_router
from prr.ui.routers.state import state_router

app = FastAPI()

static_files_directory_path = os.path.dirname(__file__) + "/static"
app.mount("/static", StaticFiles(directory=static_files_directory_path), name="static")

# reports current state of the runs
app.include_router(state_router)

# shows runs, triggers run
app.include_router(runs_router)

# shows diff between runs
app.include_router(diff_router)

# enables editing prompt files
app.include_router(edit_router)


@app.on_event("startup")
async def startup_event():
    webbrowser.open("http://localhost:8400/", new=2)


@app.get("/", response_class=RedirectResponse)
async def root(request: Request):
    return RedirectResponse("/edit", status_code=302)
