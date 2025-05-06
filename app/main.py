from fastapi import FastAPI, Body
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="FastAPI Project",
    description="A FastAPI project using Poetry",
    version="0.1.0",
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/api/chat")
async def chat(payload: dict = Body(...)):
    # For now, assume every request ends with success
    return {"status": "success"}
