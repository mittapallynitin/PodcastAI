import os


def get_env_var(key: str, default: str | None = None, required: bool = False) -> str:
    value = os.getenv(key, default)
    if required and value is None:
        raise RuntimeError(f"Missing required environment variable: {key}")
    return str(value)


# Security Configurations
SECRET_KEY = get_env_var("SECRET_KEY", required=True)
ALGORITHM = get_env_var("ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(get_env_var("ACCESS_TOKEN_EXPIRE_MINUTES", default="15"))
