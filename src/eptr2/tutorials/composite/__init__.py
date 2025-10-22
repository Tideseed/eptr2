import os
from eptr2.tutorials.main import run_app


def run_composite_app(
    username: str | None = None, password: str | None = None, port: int | None = None
):
    script_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "⭐️_Ana_Sayfa.py"
    )
    run_app(username=username, password=password, script_path=script_path, port=port)
