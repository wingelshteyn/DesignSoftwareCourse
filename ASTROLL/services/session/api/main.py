from fastapi import FastAPI

app = FastAPI(title="ASTROLL Session Service")


@app.get("/health")
def health():
    return {"status": "ok", "service": "session"}
