from fastapi import FastAPI
from app.api.input_router import router as input_router

app = FastAPI()

app.include_router(input_router, prefix="/api")