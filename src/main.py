import asyncio

from fastapi import FastAPI, WebSocket
from starlette.middleware.cors import CORSMiddleware

from src.config import config
from src.routers import router as program_router
from src.utils.closed_checker import alert_messages

app = FastAPI(title="VISIONERO", version="0.0.1")


@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        if len(alert_messages) > 0:
            message = alert_messages.pop(0)
            await websocket.send_text(message)
        await asyncio.sleep(0.01)


app.add_middleware(
    CORSMiddleware,
    allow_origins=config.origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)

ROUTERS_V1 = [program_router]

for router in ROUTERS_V1:
    app.include_router(router, prefix="/api/v1")
