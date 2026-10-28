from flask import request, abort


def parametr_int(nazwa: str, minimum: int, maksimum: int) -> int:
    wartosc_raw = request.args.get(nazwa)

    if wartosc_raw is None:
        abort(400, description=f"Brak parametru {nazwa}")

    try:
        wartosc = int(wartosc_raw)
    except (ValueError, TypeError):
        abort(400, description=f"Parametr {nazwa} musi być liczbą całkowitą")

    if wartosc < minimum or wartosc > maksimum:
        abort(422, description=f"Parametr {nazwa} poza zakresem {minimum}-{maksimum}")

    return wartosc