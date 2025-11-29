# redeploy trigger
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

    token_url = "https://www.saxo.com/oauth2/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(token_url, data=payload, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.status_code, "details": response.text}

@app.get("/api/openapi/port/v1/accounts/me")
def get_account_info(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return {"error": "Missing Authorization header"}

    url = "https://gateway.saxobank.com/openapi/port/v1/accounts/me"
    headers = {"Authorization": auth_header}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response}
