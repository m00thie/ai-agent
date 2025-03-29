from fastapi import FastAPI

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
