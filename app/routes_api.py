from flask import Blueprint, jsonify
from app.services import pobierz_zamowienia, raporty_roku
from app.validators import parametr_int
from app.decorators import wymagany_parametr

api_bp = Blueprint("api", __name__)


@api_bp.get("/kpi")
def kpi():
    zamowienia = pobierz_zamowienia("PL")
    return jsonify(region="PL", liczba_zamowien=len(zamowienia))


@api_bp.get("/raporty")
@wymagany_parametr("rok")
def raporty():
    rok = parametr_int("rok", 2020, 2030)
    raporty_list = raporty_roku(rok)
    return jsonify(rok=rok, raporty=raporty_list)