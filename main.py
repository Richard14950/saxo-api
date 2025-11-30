# Trigger redeploy – commit léger pour forcer Railway à re-provisionner le domaine

from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok", "service": "MC_ProxySaxo"}

@app.get("/token")
def get_token():
    client_id = os.getenv("SAXO_CLIENT_ID")
    client_secret = os.getenv("SAXO_CLIENT_SECRET")
    redirect_uri = os.getenv("SAXO_REDIRECT_URI")

    if not client_id or not client_secret or not redirect_uri:
        return {"error": "Missing environment variables"}

    url = "https://sim.openbankingplatform.com/sim/openapi/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": "Token request failed",
                "status_code": response.status_code,
                "details": response.text
            }
    except Exception as e:
        return {"error": str(e)}
