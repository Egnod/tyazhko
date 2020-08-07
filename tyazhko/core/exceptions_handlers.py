from fastapi import FastAPI


def set_exceptions_handlers(app: FastAPI) -> FastAPI:
    exceptions_info = {}

    for exception_class, exception_func in exceptions_info.items():
        app.add_exception_handler(exception_class, exception_func)

    return app
