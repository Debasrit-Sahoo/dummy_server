from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import os

INTERNAL_SECRET = os.environ["INTERNAL_SECRET"]
if not INTERNAL_SECRET:
    raise RuntimeError("INTERNAL_SECRET cannot be empty")

app = FastAPI(title="Internal Nuclear Code API", docs_url=None, redoc_url=None)

@app.middleware("http")
async def verify_secret_header(request: Request, call_next):
    secret = request.headers.get("X-Internal-Gateway-Auth")
    if secret != INTERNAL_SECRET:
        return JSONResponse(
            status_code=403,
            content={"detail": "Forbidden — missing or invalid internal secret"}
        )
    return await call_next(request)

@app.get("/launch-codes")
async def launch_codes():
    return {
        "codes": ["NUKE-ALPHA-123", "NUKE-BRAVO-456", "NUKE-CHARLIE-789"],
        "note": "internal use only"
    }

