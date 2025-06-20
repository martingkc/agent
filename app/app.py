from flask import Flask
from flask_cors import CORS
import debugpy
import os
from tools import tools_bp


def create_app():
    app = Flask(__name__)
    if os.getenv("DEBUG_MODE", "false").lower() == "true":
        print("Waiting for debugger to attach...")
        debugpy.listen(("0.0.0.0", 5678))
        debugpy.wait_for_client()
        print("Debugger attached")

    app.register_blueprint(tools_bp)

  

    CORS(app, supports_credentials=True, origins=["http://localhost:5000"])

    return app
