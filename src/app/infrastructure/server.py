from asgiref.wsgi import WsgiToAsgi
from flask_openapi3 import Info
from flask_openapi3 import OpenAPI

from app.settings import settings
from app.transport.routers import tasks, health, user


import ujson
from flask.json.provider import JSONProvider


class UJSONProvider(JSONProvider):
    # https://github.com/ultrajson/ultrajson
    encode_html_chars = False
    ensure_ascii = False
    indent = 4

    def dumps(self, obj, **kwargs):
        option = {
            "encode_html_chars": self.encode_html_chars,
            "ensure_ascii": self.ensure_ascii,
            "indent": self.indent,
        }
        return ujson.dumps(obj, **option)

    def loads(self, s, **kwargs):
        return ujson.loads(s)


def make_app() -> OpenAPI:
    jwt = {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}

    security_schemes = {"jwt": jwt}

    info = Info(title="Task Management API", version="1.0.0", description=settings.kot)
    app = OpenAPI("FLUSSONIC", info=info, security_schemes=security_schemes)
    app.register_api(tasks)
    app.register_api(health)
    app.register_api(user)

    ujson_provider = UJSONProvider(app)
    app.json = ujson_provider

    asgi_app = WsgiToAsgi(app)

    return asgi_app
