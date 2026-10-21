from flask import Flask, request, abort, jsonify
from services import policz_wskazniki, dostepne_regiony

app = Flask(__name__)
SCIEZKA_DANE = "dane/zamowienia.csv"


@app.get("/")
def index():
    return "Panel wskaźników"


@app.get("/kpi")
def kpi_html():
    # Pobieramy region z paska adresu
    region = request.args.get("region")

    # Sprawdzamy, czy region jest na liście dostępnych
    if region not in dostepne_regiony(SCIEZKA_DANE):
        abort(404, description=f"Nieznany region: {region}")

    # Jeśli jest ok, liczymy i zwracamy HTML
    wskazniki = policz_wskazniki(SCIEZKA_DANE, region)
    marza = wskazniki['marza']
    return f"<h1>Wskaźniki: {region}</h1><p>Marża: {marza:.2%}</p>"


@app.get("/api/kpi")
def kpi_json():
    # Ten sam proces, ale zwracamy dane w formacie JSON
    region = request.args.get("region")

    if region not in dostepne_regiony(SCIEZKA_DANE):
        abort(404, description=f"Nieznany region: {region}")

    wskazniki = policz_wskazniki(SCIEZKA_DANE, region)
    return jsonify(wskazniki)