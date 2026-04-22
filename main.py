import os
from functools import partial
import sys
import click
import dotenv
import uvicorn
from colorama import Fore, Style, init
import warnings

warnings.filterwarnings("ignore")
init(autoreset=True)

print_warning = partial(print, Fore.YELLOW + "WARNING: " + Style.RESET_ALL)
print_info    = partial(print, Fore.GREEN  + "INFO:    " + Style.RESET_ALL)

_DEFAULT_ENV  = "local"
_ENV_FOLDER   = "./env"
_ENV_FILE_MAP = {
    "dev":   ".dev.properties",
    "stage": ".stage.properties",
    "prod":  ".prod.properties",
    "local": ".local.properties",
}


@click.command()
@click.option("--env",   default="local", type=click.Choice(["local", "dev", "stage", "prod"], case_sensitive=False))
@click.option("--debug", type=click.STRING, is_flag=True, default=False)
@click.option("--port",  type=click.STRING, default="8000")
def main(env: str, debug: bool, port: str):
    if env_file := _ENV_FILE_MAP.get(env or _DEFAULT_ENV):
        env_path = f"{_ENV_FOLDER}/{env_file}"
        if dotenv.load_dotenv(env_path, override=True):
            print_info(f"EnvLoaded: {env_path}")
        else:
            print_warning(f"FailedLoadingEnv: {env_path}")

    env = os.environ.get("ENV", env)
    print_info(f"Running on env: {env}")

    from lib.core.config import config

    config.ENV      = env
    config.DEBUG    = debug is True
    config.APP_PORT = int(port) if port else config.APP_PORT

    server_workers = int(os.environ.get("RUN_APP_SERVER_WORKER", 1))
    print_info(f"FastAPI Server | env: {config.ENV} | host: {config.APP_HOST} | port: {config.APP_PORT} | workers: {server_workers}")

    uvicorn.run(
        app="lib.app.server:app",
        host=config.APP_HOST,
        port=config.APP_PORT,
        reload=config.DEBUG,
        workers=server_workers,
    )


if __name__ == "__main__":
    main()