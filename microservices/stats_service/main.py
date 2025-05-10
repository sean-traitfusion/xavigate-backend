from fastapi import FastAPI
from analytics_routes import router as analytics_router

app = FastAPI()

app.include_router(analytics_router, prefix="/stats")

@app.get("/health")
def health():
    return {"status": "ok", "service": "stats"}