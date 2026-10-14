"""Entrypoint do Community Cloud: Google e PostgreSQL obrigatórios."""
import runpy
from pathlib import Path

runpy.run_path(str(Path(__file__).with_name('app.py')), init_globals={'ROTA_CLOUD':True})
