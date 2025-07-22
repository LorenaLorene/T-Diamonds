from fastapi import FastAPI
from app.api import router

app = FastAPI(title="Public Search API Wrapper")
app.include_router(router)