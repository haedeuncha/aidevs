from fastapi import FastAPI
from app.routers.chat_router import chat_router
import app.core.chat_config  

app = FastAPI(title="Main App")

app.include_router(chat_router)

