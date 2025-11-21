# Ce code définit une API FastAPI avec trois routes :
# - /ping : vérifie que le serveur est en ligne
# - /prix : renvoie un prix fictif pour un ISIN donné
# - /positions : renvoie une liste de positions formatées pour Google Sheets

from fastapi import FastAPI

app = FastAPI()

@app.get("/ping")
def ping():
    return {"status": "ok", "message": "Saxo_Richard est en ligne"}

@app.get("/prix")
def get_prix(isin: str):
    return {"isin": isin, "prix": "123.45", "source": "fictif"}

@app.get("/positions")
def get_positions():
    positions = [
        {
            "Compte": "CTO",
            "Symbole": "IPSOS:xpar",
            "ISIN": "FR0000073298",
            "Instruments": "Ipsos",
            "Devise": "EUR",
            "Type d'actif": "Actions",
            "Prix entrée": 52.05,
            "Prix revient": 51.05,
            "Prix actuel": 32.24,
            "Date de valeur": "2025-11-14",
            "Quantité": 3,
            "Exposition (EUR)": 97,
            "% 1J": -1.23,
            "+/- Nette (EUR)": -61.75,
            "+/- (%)": -36.85
        },
        {
            "Compte": "CTO",
            "Symbole": "CHIP:xpar",
            "ISIN": "LU1900066033",
            "Instruments": "Amundi MSCI Semiconductors UCITS ETF Acc",
            "Devise": "EUR",
            "Type d'actif": "ETF",
            "Prix entrée": 56.03,
            "Prix revient": 55.49,
            "Prix actuel": 68.9,
            "Date de valeur": "2025-11-14",
            "Quantité": 15,
            "Exposition (EUR)": 1034,
            "% 1J": -3.64,
            "+/- Nette (EUR)": 191.05,
            "+/- (%)": 24.15
        }
    ]
    return {"positions": positions}

