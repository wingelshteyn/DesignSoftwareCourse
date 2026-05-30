from fastapi import FastAPI

app = FastAPI(title="ASTROLL Realtime Worker Service")


@app.get("/health")
def health():
    return {"status": "ok", "service": "realtime_worker"}
