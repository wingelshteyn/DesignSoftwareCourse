from fastapi import FastAPI

app = FastAPI(title="ASTROLL Characters Service")


@app.get("/health")
def health():
    return {"status": "ok", "service": "characters"}
