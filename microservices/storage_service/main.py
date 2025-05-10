from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from memory.data.routes import router as memory_router
from session.aq_routes import router as aq_router
from session.session_routes import router as session_router
from session.user_profile_routes import router as profile_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
# app.include_router(memory_router, prefix="/memory")
app.include_router(aq_router, prefix="/aq")
app.include_router(session_router, prefix="/session")
app.include_router(profile_router, prefix="/profile")

@app.get("/health")
def health():
    return {"status": "ok", "service": "rag"}