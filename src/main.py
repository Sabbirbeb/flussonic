from app.infrastructure.server import make_app

app = make_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9000)

    # params: dict[str, Any] = {
    #     "host": "0.0.0.0",
    # }
    # if settings.enviroment == Enviroments.local:
    #     params = {**params, "port": 9000, "reload": True}
    # else:
    #     params = {**params, "port": 9000}
    # uvicorn.run("main:app", **params)
