import os
import subprocess


def run_app(username: str, password: str, script_path: str, port: int | None = None):
    """
    Launch the Streamlit app programmatically.
    """
    # Get the absolute path of this script
    # script_path = os.path.abspath(__file__)

    os.environ["EPTR_USERNAME"] = username
    os.environ["EPTR_PASSWORD"] = password

    # Run Streamlit CLI command to start the app
    run_l = ["streamlit", "run", script_path]
    if port is not None:
        run_l.extend(["--server.port", str(port)])
    try:
        subprocess.run(run_l, check=True)
    except FileNotFoundError:
        raise RuntimeError(
            "Streamlit is not installed or not found in the PATH. Please ensure Streamlit is installed in your environment."
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to run the Streamlit app: {e}")
