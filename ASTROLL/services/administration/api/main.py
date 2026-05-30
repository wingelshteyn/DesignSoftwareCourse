from fastapi import FastAPI

app = FastAPI(title="ASTROLL Administration Service")


@app.get("/health")
def health():
    return {"status": "ok", "service": "administration"}
