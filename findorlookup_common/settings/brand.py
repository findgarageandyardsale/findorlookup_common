from typing import List, Tuple, TypedDict


class Brand(TypedDict, total=False):
    app_name: str
    logo_url: str
    support_email: str
    primary_color: str
    app_url: str
    # Optional, used by richer templates:
    tagline: str                               # "Find your next car near you."
    welcome_steps: List[Tuple[str, str]]       # [(step title, step body), ...]
