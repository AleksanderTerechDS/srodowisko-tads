from flask import Blueprint, abort, request, redirect, url_for
from app.services import dostepne_regiony, pobierz_zamowienia, raporty_roku, zapisz_raport

panel_bp = Blueprint("panel", __name__)

ROK_DOMYSLNY = 2026


# --- TRASY Z ĆWICZEŃ 2 ---

@panel_bp.get("/")
def index():
    return "<h1>Panel główny</h1>"


@panel_bp.get("/kpi")
def kpi():
    region_param = request.args.get("region")
    wykaz = dostepne_regiony() if callable(dostepne_regiony) else dostepne_regiony
    if region_param and region_param not in wykaz:
        abort(404, description=f"Nieznany region: {region_param}")
    return f"<h1>KPI dla regionu {region_param}</h1>" if region_param else "<h1>KPI</h1>"


# --- ZADANIE 1: TRASY ZASOBOWE I KONWERTERY ---

@panel_bp.get("/regiony/<region:kod>")
def region(kod: str):
    wykaz = dostepne_regiony() if callable(dostepne_regiony) else dostepne_regiony
    if kod not in wykaz:
        abort(404, description=f"Nieznany region: {kod}")

    zamowienia = pobierz_zamowienia(kod) if callable(pobierz_zamowienia) else []
    liczba = len(zamowienia)
    return f"<h1>Region {kod}</h1><p>Zamówień: {liczba}</p>"


@panel_bp.get("/raporty/", defaults={"rok": ROK_DOMYSLNY})
@panel_bp.get("/raporty/<int(min=2020, max=2030):rok>")
def raport(rok: int):
    n = len(raporty_roku(rok))
    return f"<h1>Raport {rok}</h1><p>Zapisane raporty: {n}</p>"


# --- ZADANIE 2: METODY, PRZEKIEROWANIA I WALIDACJA ---

@panel_bp.route("/raporty/nowy", methods=["GET", "POST"])
def nowy_raport():
    if request.method == "GET":
        return "Instrukcja zapisu raportu: wyślij formularz POST z polami 'rok' oraz 'region'."

    # Pobranie i konwersja pola rok (zwraca None, gdy brak lub błąd konwersji)
    rok = request.form.get("rok", type=int)
    region_val = request.form.get("region")

    wykaz = dostepne_regiony() if callable(dostepne_regiony) else dostepne_regiony

    # Walidacja: brak liczby w roku lub nieistniejący region -> 400
    if rok is None or region_val not in wykaz:
        abort(400, description="Niepoprawne dane formularza")

    # Walidacja: rok poza zakresem -> 422
    if rok < 2020 or rok > 2030:
        abort(422, description="Rok poza zakresem 2020-2030")

    # Zapis i przekierowanie PRG (303)
    zapisz_raport(rok, region_val)
    return redirect(url_for("panel.raport", rok=rok), code=303)


@panel_bp.get("/stary-panel")
def stary_panel():
    return redirect(url_for("panel.kpi"), code=301)