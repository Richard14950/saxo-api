import os
import json
import requests
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse

app = FastAPI(title="MC_ProxySaxo")

SAXO_CLIENT_ID     = os.getenv("SAXO_CLIENT_ID")
SAXO_CLIENT_SECRET = os.getenv("SAXO_CLIENT_SECRET")
SAXO_REDIRECT_URI  = os.getenv("SAXO_REDIRECT_URI", "https://localhost")

TOKEN_URL = "https://openapi.saxobank.com/authentication/v1/token"
BASE_URL  = "https://openapi.saxobank.com"


@app.get("/")
def root():
    return {"status": "ok", "service": "MC_ProxySaxo"}


def fetch_token():
    """Fonction interne pour récupérer un access_token depuis Saxo"""
    payload = {
        "grant_type": "client_credentials",
        "client_id": SAXO_CLIENT_ID,
        "client_secret": SAXO_CLIENT_SECRET,
        "redirect_uri": SAXO_REDIRECT_URI
    }
    try:
        r = requests.post(TOKEN_URL, data=payload, timeout=20)
        if r.status_code != 200:
            return None, r.status_code, r.text
        token_data = r.json()
        return token_data.get("access_token"), 200, None
    except Exception as e:
        return None, 502, str(e)


@app.get("/token")
def get_token():
    access_token, status, error = fetch_token()
    if not access_token:
        return JSONResponse(status_code=status, content={"error": error or "Token fetch failed"})
    return {"access_token": access_token}


@app.get("/api/{path:path}")
def proxy_api(path: str):
    access_token, status, error = fetch_token()
    if not access_token:
        return JSONResponse(status_code=status, content={"error": error or "Token fetch failed"})

    url = f"{BASE_URL}/{path.lstrip('/')}"
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        r = requests.get(url, headers=headers, timeout=20)
        return Response(content=r.content,
                        media_type=r.headers.get("Content-Type", "application/json"),
                        status_code=r.status_code)
    except Exception as e:
        return JSONResponse(status_code=502, content={"error": f"Proxy API failed: {str(e)}"})
