# Saxo OpenAPI sandbox – correction du domaine OAuth2 et payload
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
    # Optionnel selon tes besoins et configuration d’app
    scope = os.getenv("SAXO_SCOPE", "read,trade")

    if not client_id or not client_secret:
        return {"error": "Missing environment variables"}

    # Base sandbox OpenAPI (sim) – corriger ici si tu as une valeur spécifique fournie par Saxo
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
        # Retourne le JSON ou détaille l’erreur
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
