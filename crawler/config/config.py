import json
import os


def config():
    PYTHON_ENV = os.getenv("PYTHON_ENV", default="DEV")
    if PYTHON_ENV == "DEV":
        with open("/Users/terry/workspace/study/holiday-pharmacy/crawler/config/config-dev.json") as f:
            config = json.load(f)
            host = config["database_host"]
            name = config["database_name"]
            user = config["database_user"]
            _pass = config["database_pass"]
    elif PYTHON_ENV == "PRD":
        host = os.getenv("database_host")
        name = os.getenv("database_name")
        user = os.getenv("database_user")
        _pass = os.getenv("database_pass")

    return {"host": host, "name": name, "user": user, "pass": _pass}
