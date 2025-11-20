from fastapi import FastAPI

app = FastAPI()

@app.get("/ping")
def ping():
    return {"status": "ok", "message": "Saxo_Richard est en ligne"}

@app.get("/prix")
def get_prix(isin: str):
    return {"isin": isin, "prix": "123.45", "source": "fictif"}
