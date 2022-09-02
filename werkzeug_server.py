

from werkzeug.serving import run_simple
from app import create_app

app = create_app()

run_simple("0.0.0.0", 5001, app, use_debugger=True)


