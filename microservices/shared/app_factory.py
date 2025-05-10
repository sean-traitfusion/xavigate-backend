def create_app() -> FastAPI:
    app = FastAPI()
    app.add_middleware(...)
    return app