import logging
import time
from flask import Flask, g
from .config import KONFIGURACJE
from .converters import RegionConverter
from .errors import zarejestruj_obsluge_bledow


def create_app(nazwa_konfiguracji="rozwojowa"):
    app = Flask(__name__)

    # 1. Konwerter zarejestrowany przed blueprintami
    app.url_map.converters["region"] = RegionConverter

    app.config.from_object(KONFIGURACJE[nazwa_konfiguracji])
    app.logger.setLevel(logging.INFO)

    # 2. Procedury cyklu (before_request & after_request)
    @app.before_request
    def start_timer():
        g.start = time.perf_counter()

    @app.after_request
    def add_header(response):
        if hasattr(g, "start"):
            czas = (time.perf_counter() - g.start) * 1000
            response.headers["X-Czas-Ms"] = f"{czas:.2f}"
        return response

    # 3. Obsługa błędów
    zarejestruj_obsluge_bledow(app)

    # 4. Blueprinty i wersjonowanie
    from .routes_api import api_bp
    from .routes_panel import panel_bp

    app.register_blueprint(panel_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(api_bp, url_prefix="/api/v2", name="api_v2")

    return app