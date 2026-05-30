from fastapi import FastAPI

app = FastAPI(title="ASTROLL Dice Service")


@app.get("/health")
def health():
    return {"status": "ok", "service": "dice"}
