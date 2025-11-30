# Saxo Proxy + Diagnostic IP – version complète et non destructive

from fastapi import FastAPI
import os
import requests

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok", "service": "MC_ProxySaxo"}

@app.get("/token")
def get_token():
    client_id = os.getenv("SAXO_CLIENT_ID")
    client_secret = os.getenv("SAXO_CLIENT_SECRET")
    scope = os.getenv("SAXO_SCOPE", "read,trade")

    if not client_id or not client_secret:
        return {"error": "Missing environment variables"}

    base = os.getenv("SAXO_BASE", "https://sim.openapi.saxobank.com")
    url = f"{base}/oauth2/token"

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": scope,
    }

    try:
        r = requests.post(url, headers=headers, data=data, timeout=20)
        if r.headers.get("content-type", "").startswith("application/json"):
            payload = r.json()
        else:
            payload = {"raw": r.text}

        if r.status_code == 200:
            return payload
        return {
            "error": "Token request failed",
            "status_code": r.status_code,
            "details": payload
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/ip")
def get_ip():
    try:
        r = requests.get("https://api.ipify.org?format=json", timeout=10)
        return r.json()
    except Exception as e:
        return {"error": str(e)}
