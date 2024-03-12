from typing import Any

import uvicorn

from app.infrastructure.server import make_app
from app.settings import settings, Enviroments

app = make_app()

if __name__ == "__main__":
    params: dict[str, Any] = {
        "host": "0.0.0.0",
    }
    if settings.enviroment == Enviroments.local:
        params = {**params, "port": 9000, "reload": True}
    else:
        params = {**params, "port": 9000}

    uvicorn.run("main:app", **params)
