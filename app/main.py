from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI(
    title="FastAPI Project",
    description="A FastAPI project using Poetry",
    version="0.1.0",
)

@app.get("/")
async def root():
    return RedirectResponse(url="/health")

@app.get("/health")
async def health():
    return {"status": "ok"}
