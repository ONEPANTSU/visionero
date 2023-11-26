import uvicorn

from src.database import init_database
from src.main import app
from src.config import config

if __name__ == "__main__":
    init_database(config.database)
    uvicorn.run(
        app,
        host=config.app.host,
        port=config.app.port
    )
