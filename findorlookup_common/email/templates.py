from typing import Callable, TypedDict

from findorlookup_common.settings.brand import Brand
from findorlookup_common.email.layout import (
    btn,
    fallback,
    first_name,
    h1,
    info_table,
    layout,
    p,
    small,
    step,
    warning_box,
)


class Rendered(TypedDict):
    subject: str
    html: str


def _steps_block(brand: Brand) -> str:
    steps = brand.get("welcome_steps") or []
    if not steps:
        return ""
    rendered = "".join(
        step(brand, i + 1, title, body) for i, (title, body) in enumerate(steps)
    )
    return (
        '<table width="100%" cellpadding="0" cellspacing="0" border="0" '
        'style="margin:24px 0;">' + rendered + "</table>"
    )


def verify_email(brand: Brand, *, name: str, token: str) -> Rendered:
    url = f"{brand['app_url']}/verify-email?token={token}"
    body = (
        h1("Confirm your email address")
        + p(
            f"Hi {first_name(name)}, you're one tap from unlocking {brand['app_name']}. "
            "Confirm your email so we can keep your account secure and send you only the alerts you ask for."
        )
        + btn(brand, url, "Confirm email address")
        + fallback(url, "24 hours")
        + small(
            f"If you did not create a {brand['app_name']} account, ignore this email "
            "and nothing further will happen."
        )
    )
    return {
        "subject": f"Confirm your email for {brand['app_name']}",
        "html": layout(brand, "Verify Email", body),
    }


def welcome(brand: Brand, *, name: str) -> Rendered:
    tagline = brand.get("tagline") or f"Welcome to {brand['app_name']}"
    intro = (
        f"Hi {first_name(name)}, your account is live. "
        f"Here's how most people get the most out of {brand['app_name']}:"
    )
    body = (
        h1(tagline)
        + p(intro)
        + _steps_block(brand)
        + btn(brand, brand["app_url"], f"Open {brand['app_name']}")
    )
    return {
        # Transactional subject (deliverable), benefit tagline lives in the H1.
        "subject": f"Your {brand['app_name']} account is ready — getting started",
        "html": layout(brand, "Welcome", body),
    }


def login_notification(
    brand: Brand, *, email: str, ip: str, time: str, user_agent: str
) -> Rendered:
    rows = []
    if time:
        rows.append(("Time", time))
    if ip:
        rows.append(("IP Address", ip))
    if user_agent:
        rows.append(("Device", user_agent))
    body = (
        h1("New sign-in to your account")
        + p(
            f"We recorded a new sign-in to the {brand['app_name']} account registered to {email}."
        )
        + (info_table(rows) if rows else "")
        + p(
            "If this was you, nothing more to do. "
            "If you don't recognise it, reset your password now and we'll end every active session."
        )
        + btn(brand, f"{brand['app_url']}/reset-password", "Reset my password")
        + small("Location is estimated from IP and may not be exact.")
    )
    return {
        "subject": f"New sign-in to your {brand['app_name']} account",
        "html": layout(brand, "New Sign-In", body, recipient_email=email),
    }


def reset_password(brand: Brand, *, email: str, token: str) -> Rendered:
    from urllib.parse import quote

    url = f"{brand['app_url']}/reset-password?token={token}&email={quote(email)}"
    body = (
        h1("Reset your password")
        + p(
            f"We received a request to reset the password for {email}. "
            "If this was you, set a new one in the next 30 minutes."
        )
        + btn(brand, url, "Choose a new password")
        + warning_box(
            "<strong>This link expires in 30 minutes.</strong> "
            "After that, request a fresh one from the sign-in screen."
        )
        + fallback(url, "30 minutes")
        + small(
            "If you did not request a password reset, ignore this email. "
            "Your password will not change."
        )
    )
    return {
        "subject": f"Reset your {brand['app_name']} password",
        "html": layout(brand, "Reset Your Password", body, recipient_email=email),
    }


def payment_success(
    brand: Brand,
    *,
    name: str,
    amount: str,
    listing_title: str,
    receipt_url: str = "",
) -> Rendered:
    body = (
        h1("Payment received — you're live")
        + p(
            f"Hi {first_name(name)}, your payment of {amount} is in, and "
            f"\"{listing_title}\" is now visible on {brand['app_name']}."
        )
        + info_table([("Amount", amount), ("Listing", listing_title)])
        + btn(brand, brand["app_url"], "View my listing")
        + p(
            "Expect your first replies within a few hours. "
            "Responding fast is the single biggest thing you can do — "
            "the first provider to reply usually wins the job."
        )
    )
    if receipt_url:
        body += p(
            f'<a href="{receipt_url}" style="color:#1D4ED8;">Download your receipt</a>'
        )
    return {
        "subject": f"Payment confirmed — {brand['app_name']}",
        "html": layout(brand, "Payment Confirmed", body),
    }


TEMPLATES: dict[str, Callable[..., Rendered]] = {
    "verify_email": verify_email,
    "welcome": welcome,
    "login_notification": login_notification,
    "reset_password": reset_password,
    "payment_success": payment_success,
}
