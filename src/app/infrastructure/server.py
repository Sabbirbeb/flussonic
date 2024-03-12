from asgiref.wsgi import WsgiToAsgi
from flask_openapi3 import Info
from flask_openapi3 import OpenAPI

from app.settings import settings
from app.transport.routers import tasks

def make_app() -> OpenAPI:
    jwt = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT"
        }

    security_schemes = {"jwt": jwt}

    info = Info(title="Task Management API", version="1.0.0", description=settings.kot)
    app = OpenAPI("FLUSSONIC", info=info, security_schemes=security_schemes)
    app.register_api(tasks)

    app.get("/q")

    asgi_app = WsgiToAsgi(app)

    return asgi_app