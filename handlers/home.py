from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Initialize Jinja2Templates
templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="",
    tags=["Home"]
)

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("tasks.html", {"request": request})