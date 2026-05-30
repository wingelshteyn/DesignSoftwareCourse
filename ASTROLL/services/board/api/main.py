from fastapi import FastAPI

app = FastAPI(title="ASTROLL Board Service")


@app.get("/health")
def health():
    return {"status": "ok", "service": "board"}
