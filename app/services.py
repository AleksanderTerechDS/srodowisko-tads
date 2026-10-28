import csv
from pathlib import Path

PLIK_DANYCH = Path(__file__).resolve().parent.parent / "dane" / "zamowienia.csv"

# --- ZADANIE 1: MAGAZYN RAPORTÓW W PAMIĘCI ---

lista_RAPORTY = []


def zapisz_raport(rok: int, region: str) -> dict:
    raport = {"rok": int(rok), "region": str(region)}
    lista_RAPORTY.append(raport)
    return raport


def raporty_roku(rok: int) -> list:
    return [r for r in lista_RAPORTY if r["rok"] == int(rok)]


# --- WARSTWA USŁUG ---

def dostepne_regiony(*args, **kwargs) -> list:
    return ["PL", "DE", "CZ"]


def pobierz_zamowienia(region: str = None) -> list:
    if PLIK_DANYCH.is_file():
        zamowienia = []
        with open(PLIK_DANYCH, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if region is None or row.get("region") == region:
                    zamowienia.append(row)
        return zamowienia

    mock_dane = {
        "PL": [{"id": 1}, {"id": 2}, {"id": 3}],
        "DE": [{"id": 4}, {"id": 5}, {"id": 6}],
        "CZ": [{"id": 7}, {"id": 8}],
    }
    if region:
        return mock_dane.get(region, [])
    return [z for lista in mock_dane.values() for z in lista]


def policz_wskazniki(region: str = None) -> dict:
    zamowienia = pobierz_zamowienia(region)
    return {
        "region": region,
        "liczba_zamowien": len(zamowienia)
    }