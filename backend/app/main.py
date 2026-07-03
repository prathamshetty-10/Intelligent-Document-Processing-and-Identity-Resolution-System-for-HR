from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.upload import router as upload_router

app = FastAPI(
    title="HR Document Extraction API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)


@app.get("/")
def root():
    return {
        "message": "HR Document Extraction API Running"
    }