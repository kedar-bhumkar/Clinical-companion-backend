from fastapi import FastAPI, Request
import time
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from constants import *
from service import handlemessage, handle_config
from pydantic_models import Message

theResponse = {"hello"}

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server startup .....")    
    yield
    print("Server shutdown .......")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    print(f"Request took {process_time} secs to complete")
    return response

@app.get("/")
def doGet(request: Request):
    return {"Hello": "World"}

@app.post("/chat")
async def doChat(request: Request, message: Message):
    print("Inside /chat")
    print(f'prompt - {message.entity}, mode - {message.message}')

    response = await handlemessage(message)
    return {"llm_response": response}

@app.post("/config")
def doConfig(request: Request, message: Message):
    print("Inside /config")
    print(f'prompt - {message.entity}, mode - {message.message}')

    response = handle_config(message)
    return {"llm_response": response}