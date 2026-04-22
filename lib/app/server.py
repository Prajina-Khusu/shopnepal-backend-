from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from lib.core.config import config
from lib.app.adapter.input.api.v1 import router
from lib.app.container import Container


def init_routers(app_: FastAPI) -> None:
    app_.include_router(router)


def create_app() -> FastAPI:

    # Create and wire container first
    container = Container()

    app_ = FastAPI(
        title="ShopNepal API",
        description="Backend API for ShopNepal Ecommerce",
        version="1.0.0",
        docs_url="/docs"     if config.RUN_APP_ENABLE_DOCS else None,
        openapi_url="/openapi.json" if config.RUN_APP_ENABLE_DOCS else None,
    )

    app_.container = container
    container.wire(packages=["lib.app"])

    app_.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    init_routers(app_)

    return app_


app = create_app()


@app.get("/health")
async def health_check():
    return JSONResponse(
        content={
            "status": "ShopNepal API is running ✅",
            "env":    config.ENV,
            "debug":  config.DEBUG,
        },
        status_code=200,
    )