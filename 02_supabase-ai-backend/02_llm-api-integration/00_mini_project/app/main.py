from fastapi import FastAPI
from app.routers.chat_router import chat_router

app = FastAPI("Main App")
app.include_router(chat_router)

