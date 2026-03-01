from flask import Flask
from flask_socketio import SocketIO
from dashboard.routes import register_routes
from config.settings import SECRET_KEY

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["SECRET_KEY"] = SECRET_KEY

socketio = SocketIO(
    app,
    async_mode="threading",  
    cors_allowed_origins="*",
    logger=False,
    engineio_logger=False,
)

register_routes(app)

def get_socketio():
    return socketio
