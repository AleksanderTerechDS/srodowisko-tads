import csv


def wczytaj_zamowienia(sciezka):
    zamowienia = []
    with open(sciezka, mode='r', encoding='utf-8') as plik:
        # csv.DictReader automatycznie użyje pierwszego wiersza jako kluczy słownika
        reader = csv.DictReader(plik, skipinitialspace=True)
        for wiersz in reader:
            # Usuwamy ewentualne spacje wokół regionu i rzutujemy kwoty na float
            wiersz['region'] = wiersz['region'].strip()
            wiersz['przychod'] = float(wiersz['przychod'])
            wiersz['koszt'] = float(wiersz['koszt'])
            zamowienia.append(wiersz)
    return zamowienia


def dostepne_regiony(sciezka):
    zamowienia = wczytaj_zamowienia(sciezka)
    # Używamy zbioru (set), aby otrzymać tylko unikalne regiony
    regiony = {wiersz['region'] for wiersz in zamowienia}
    return sorted(list(regiony))


def policz_wskazniki(sciezka, region=None):
    zamowienia = wczytaj_zamowienia(sciezka)

    # Jeśli podano region, filtrujemy listę zamówień
    if region:
        zamowienia = [w for w in zamowienia if w['region'] == region]

    liczba_zamowien = len(zamowienia)
    przychod = sum(w['przychod'] for w in zamowienia)
    koszt = sum(w['koszt'] for w in zamowienia)

    # Wyliczanie marży z zabezpieczeniem przed dzieleniem przez 0
    if przychod > 0:
        marza = round((przychod - koszt) / przychod, 4)
    else:
        marza = 0.0

    return {
        "region": region,
        "liczba_zamowien": liczba_zamowien,
        "przychod": przychod,
        "koszt": koszt,
        "marza": marza
    }