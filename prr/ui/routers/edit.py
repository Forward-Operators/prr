import hashlib
import os

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates

from prr.prompt.prompt_loader import PromptConfigLoader
from prr.ui.prompt_files import PromptFiles

edit_router = APIRouter()

templates = Jinja2Templates(directory=(os.path.dirname(__file__) + "/../templates"))


class EditRenderer:
    def __init__(self, prompt_path):
        self.prompt_path = prompt_path

        loader = PromptConfigLoader()
        prompt_config = loader.load_from_path(self.prompt_path)

        self.prompt_files = PromptFiles(self.prompt_path)

    def default_file_id(self):
        return hashlib.md5(self.prompt_path.encode()).hexdigest()

    def args_for_edit(self, request, file_id=None):
        current_file_id = file_id

        if current_file_id == None:
            current_file_id = self.default_file_id()

        current_file_path = self.prompt_files.get_file_path(current_file_id)
        file_content = self.prompt_files.get_file_contents(current_file_id)

        return {
            "action": "edit",
            "request": request,
            "files": self.prompt_files.files,
            "current_file_id": current_file_id,
            "file_content": file_content,
            "prompt_name": self.prompt_name(),
            "page_title": f"Editing {self.prompt_name()}",
        }

    def edit(self, request, file_id=None):
        if len(self.prompt_files.files) == 0:
            message = "No files found"

            args = {"request": request, "page_title": message, "error_message": message}

            return templates.TemplateResponse("error.html", args)

        args = self.args_for_edit(request, file_id)

        return templates.TemplateResponse("edit.html", args)

    def update(self, request, data, file_id=None):
        content = data["content"]

        self.prompt_files.update_file(file_id, content)

        return Response("lol", media_type="text/plain")

    def prompt_name(self):
        return os.path.basename(self.prompt_path)


renderer = EditRenderer(os.environ["__PRR_WEB_UI_PROMPT_PATH"])


@edit_router.get("/edit", response_class=HTMLResponse)
async def edit_index(request: Request):
    return renderer.edit(request)


@edit_router.get("/edit/{file_id}", response_class=HTMLResponse)
async def edit(request: Request, file_id: str):
    return renderer.edit(request, file_id)


@edit_router.post("/edit/{file_id}", response_class=HTMLResponse)
async def update(request: Request, file_id: str):
    data = await request.json()
    return renderer.update(request, data, file_id)
