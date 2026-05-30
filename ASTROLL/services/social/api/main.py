from fastapi import FastAPI

app = FastAPI(title="ASTROLL Social Service")


@app.get("/health")
def health():
    return {"status": "ok", "service": "social"}
