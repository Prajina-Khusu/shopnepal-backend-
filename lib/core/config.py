import os
from dotenv import load_dotenv

_DEFAULT_ENV                     = "local"
_DEFAULT_APP_HOST                = "0.0.0.0"
_DEFAULT_APP_PORT                = 8000
_DEFAULT_SECRET_KEY              = "changethisinsecretkeyinproduction"
_DEFAULT_ALGORITHM               = "HS256"
_DEFAULT_ACCESS_TOKEN_EXPIRE_MIN = 1440  # 24 hours


class Config:

    # Server
    ENV:      str  = os.environ.get("ENV",      _DEFAULT_ENV).casefold()
    DEBUG:    bool = True
    APP_HOST: str  = os.environ.get("APP_HOST", _DEFAULT_APP_HOST)
    APP_PORT: int  = int(os.environ.get("APP_PORT", _DEFAULT_APP_PORT))

    # Database
    DATABASE_URL: str = os.environ.get("DATABASE_URL")

    # JWT / Security
    SECRET_KEY:                  str = os.environ.get("SECRET_KEY",                  _DEFAULT_SECRET_KEY)
    ALGORITHM:                   str = os.environ.get("ALGORITHM",                   _DEFAULT_ALGORITHM)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", _DEFAULT_ACCESS_TOKEN_EXPIRE_MIN))

    # Cloudinary
    CLOUDINARY_CLOUD_NAME: str = os.environ.get("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY:    str = os.environ.get("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET: str = os.environ.get("CLOUDINARY_API_SECRET")

    # Redis
    REDIS_URL: str = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

    # Docs
    RUN_APP_ENABLE_DOCS: bool = (
        os.environ.get("RUN_APP_ENABLE_DOCS", "true").casefold() == "true"
    )


class DevConfig(Config):
    DEBUG: bool = False


class LocalConfig(Config):
    DEBUG: bool = True


class StageConfig(Config):
    DEBUG: bool = False


class ProductionConfig(Config):
    DEBUG: bool = False


def get_config() -> Config:
    env = os.getenv("ENV", "local").strip().casefold()
    config_type = {
        "dev":   DevConfig(),
        "local": LocalConfig(),
        "stage": StageConfig(),
        "prod":  ProductionConfig(),
    }
    return config_type.get(env, LocalConfig())


config: Config = get_config()