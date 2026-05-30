from fastapi import FastAPI

app = FastAPI(title="ASTROLL Auth Accounts Service")


@app.get("/health")
def health():
    return {"status": "ok", "service": "auth_accounts"}
