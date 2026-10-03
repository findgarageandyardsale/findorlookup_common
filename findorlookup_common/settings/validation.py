import os
from typing import Iterable

from django.core.exceptions import ImproperlyConfigured


def validate_prod_env(required: Iterable[str]) -> None:
    if os.environ.get("DJANGO_ENV", "development") != "production":
        return
    missing = [name for name in required if not os.environ.get(name)]
    if missing:
        raise ImproperlyConfigured(
            "Missing required environment variables in production: "
            + ", ".join(missing)
        )
