from typing import Any, Iterable

from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags

from findorlookup_common.settings.brand import Brand
from findorlookup_common.email.templates import TEMPLATES


def send_branded(
    brand: Brand,
    template_name: str,
    context: dict[str, Any],
    to: str | Iterable[str],
) -> int:
    render = TEMPLATES[template_name]
    rendered = render(brand, **context)

    from_header = f"{brand['app_name']} <noreply@findorlookup.com>"
    reply_to = [brand["support_email"]]
    recipients = [to] if isinstance(to, str) else list(to)

    message = EmailMultiAlternatives(
        subject=rendered["subject"],
        body=strip_tags(rendered["html"]),
        from_email=from_header,
        to=recipients,
        reply_to=reply_to,
    )
    message.attach_alternative(rendered["html"], "text/html")
    return message.send()
