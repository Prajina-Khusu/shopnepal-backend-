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


def print_urls(host: str, port: int):
    base = f"http://localhost:{port}"
    print("\n" + Fore.CYAN + "═" * 50 + Style.RESET_ALL)
    print(Fore.CYAN + "  🚀 ShopNepal API is running!" + Style.RESET_ALL)
    print(Fore.CYAN + "═" * 50 + Style.RESET_ALL)
    print(Fore.GREEN + f"  📖 Docs:    {base}/api/v1/docs" + Style.RESET_ALL)
    print(Fore.GREEN + f"  📋 Redoc:   {base}/api/v1/redoc" + Style.RESET_ALL)
    print(Fore.GREEN + f"  ❤️  Health:  {base}/health" + Style.RESET_ALL)
    print(Fore.GREEN + f"  🔗 Base:    {base}/api/v1/" + Style.RESET_ALL)
    print(Fore.CYAN + "═" * 50 + Style.RESET_ALL)
    print(Fore.YELLOW + "\n  Endpoints:" + Style.RESET_ALL)
    print(f"  POST  {base}/api/v1/auth/register")
    print(f"  POST  {base}/api/v1/auth/login")
    print(f"  GET   {base}/api/v1/auth/me")
    print(f"  GET   {base}/api/v1/products/")
    print(f"  GET   {base}/api/v1/categories/")
    print(f"  GET   {base}/api/v1/cart/")
    print(f"  POST  {base}/api/v1/orders/checkout")
    print(f"  GET   {base}/api/v1/orders/")
    print(f"  GET   {base}/api/v1/reviews/{{product_id}}")
    print(Fore.CYAN + "═" * 50 + Style.RESET_ALL + "\n")


@click.command()
@click.option("--env",  default="local", type=click.Choice(["local", "dev", "stage", "prod"], case_sensitive=False))
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

    from lib.core.config import config
    config.ENV      = env
    config.DEBUG    = debug is True
    config.APP_PORT = int(port) if port else config.APP_PORT

    server_workers = int(os.environ.get("RUN_APP_SERVER_WORKER", 1))

    # Print all URLs
    print_urls(config.APP_HOST, int(port))

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