from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router

app = FastAPI(
    title="UK Wind Forecast Dashboard",
    description="Wind generation forecast and accuracy analysis",
    version="1.0.0",
)

# React will run on a different port during local development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")


@app.get("/")
def root():
    return {
        "message": "UK Wind Forecast API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }