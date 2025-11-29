# MC_ProxySaxo.py — proxy Saxo compatible Apps Script via Render
# Expose :
#   - GET /           → healthcheck
#   - GET /token      → retourne { "access_token": "..." }
#   - GET /api/{path} → relai vers Saxo avec Bearer token

import os
import requests
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse

app = FastAPI(title="MC_ProxySaxo")

# 🔐 Variables d'environnement (Render → Settings → Environment)
SAXO_CLIENT_ID     = os.getenv("SAXO_CLIENT_ID")
SAXO_CLIENT_SECRET = os.getenv("SAXO_CLIENT_SECRET")
SAXO_REDIRECT_URI  = os.getenv("SAXO_REDIRECT_URI", "https://localhost")

# 🌐 Endpoints officiels Saxo
TOKEN_URL = "https://openapi.saxobank.com/authentication/v1/token"
BASE_URL  = "https://openapi.saxobank.com"

@app.get("/")
def root():
    return {"status": "ok", "service": "MC_ProxySaxo"}

@app.get("/token")
def get_token():
    payload = {
        "grant_type": "client_credentials",
        "client_id": SAXO_CLIENT_ID,
        "client_secret": SAXO_CLIENT_SECRET,
        "redirect_uri": SAXO_REDIRECT_URI
    }
    try:
        r = requests.post(TOKEN_URL, data=payload, timeout=20)
        return Response(content=r.content, media_type=r.headers.get("Content-Type", "application/json"), status_code=r.status_code)
    except Exception as e:
        return JSONResponse(status_code=502, content={"error": f"Token fetch failed: {str(e)}"})

@app.get("/api/{path:path}")
def proxy_api(path: str):
    # 1) Récupère un token
    token_resp = get_token()
    if isinstance(token_resp, JSONResponse) and token_resp.status_code >= 400:
        return token_resp

    try:
        token_json = token_resp.body.decode("utf-8")
        token_data = requests.models.complexjson.loads(token_json)
        access_token = token_data.get("access_token")
    except Exception:
        return JSONResponse(status_code=500, content={"error": "Parsing access_token échoué"})

    if not access_token:
        return JSONResponse(status_code=401, content={"error": "Token absent"})

    # 2) Relai GET vers Saxo
    url = f"{BASE_URL}/{path.lstrip('/')}"
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        r = requests.get(url, headers=headers, timeout=20)
        return Response(content=r.content, media_type=r.headers.get("Content-Type", "application/json"), status_code=r.status_code)
    except Exception as e:
        return JSONResponse(status_code=502, content={"error": f"Proxy API failed: {str(e)}"})
