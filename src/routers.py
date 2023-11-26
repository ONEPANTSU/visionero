from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse, JSONResponse
from starlette.templating import Jinja2Templates

from src.config import config
from src.service import ProgramService

router = APIRouter(
    prefix="/programs",
    tags=["Programs"],
)

program_service = ProgramService()
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"app": config.app, "request": request})


@router.get("/program_status")
async def get_programs() -> JSONResponse:
    result = program_service.get_programs()
    return JSONResponse(content=result)


@router.post("/start/{program_name}")
async def start_program(program_name: str) -> JSONResponse:
    result = await program_service.start_program(program_name)
    return JSONResponse(content=result)


@router.post("/stop/{program_name}")
async def stop_program(program_name: str) -> JSONResponse:
    result = program_service.stop_program(program_name)
    return JSONResponse(content=result)


@router.post("/stop_all")
async def stop_all_programs() -> JSONResponse:
    result = program_service.stop_all_programs()
    return JSONResponse(content=result)


@router.get("/history")
async def get_history() -> JSONResponse:
    result = await program_service.get_history()
    return JSONResponse(content=result)
