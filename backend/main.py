from dotenv import load_dotenv

from app.config import DATA_DIR, STATIC_DIR

load_dotenv()

import logging
import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.api import api_router
from auth.routers import auth_router
from app.middlewares.frontend import FrontendProxyMiddleware

servers = []
app_name = os.getenv("FLY_APP_NAME")
if app_name:
    servers = [{"url": f"https://{app_name}.fly.dev"}]
app = FastAPI(servers=servers)

environment = os.getenv("ENVIRONMENT", "dev")  # Default to 'development' if not set
frontend_endpoint = os.getenv("FRONTEND_ENDPOINT")
logger = logging.getLogger("uvicorn")

logger.info(f"Environment is '{environment}'")

# Add CORS middleware for development
if environment == "dev":
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex="http://localhost:\d+|http://0\.0\.0\.0:\d+",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[frontend_endpoint],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def mount_static_files(directory, path, html=False):
    if os.path.exists(directory):
        logger.info(f"Mounting static files '{directory}' at '{path}'")
        app.mount(
            path,
            StaticFiles(directory=directory, check_dir=False, html=html),
            name=f"{directory}-static",
        )


app.include_router(api_router)
app.include_router(auth_router)

# Mount the data files to serve the file viewer
mount_static_files(DATA_DIR, "/api/files/data")
# Mount the output files from tools
mount_static_files("output", "/api/files/output")

if environment == "dev":
    if frontend_endpoint:
        app.add_middleware(
            FrontendProxyMiddleware,
            frontend_endpoint=frontend_endpoint,
            excluded_paths=set(
                route.path for route in app.routes if hasattr(route, "path")
            ),
        )
    else:
        logger.warning("No frontend endpoint - starting API server only")

        @app.get("/")
        async def redirect_to_docs():
            return RedirectResponse(url="/docs")
else:
    # Mount the frontend static files (production)
    mount_static_files(STATIC_DIR, "/", html=True)

if __name__ == "__main__":
    app_host = os.getenv("APP_HOST", "0.0.0.0")
    app_port = int(os.getenv("APP_PORT", "8000"))
    reload = True if environment == "dev" else False

    uvicorn.run(app="main:app", host=app_host, port=app_port, reload=reload)
