from fastapi import FastAPI
from app.api import router

app = FastAPI(title="Tracr Integration – Diamond Carat Weight Tracker")
app.include_router(router)
