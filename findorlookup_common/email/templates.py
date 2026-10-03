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


def verify_email(brand: Brand, *, name: str, token: str) -> Rendered:
    url = f"{brand['app_url']}/verify-email?token={token}"
    body = (
        h1("Confirm your email address")
        + p(
            f"Hi {first_name(name)}, you're one click away. "
            f"Confirm your email address to activate your {brand['app_name']} account."
        )
        + btn(brand, url, "Confirm email address")
        + fallback(url, "24 hours")
        + small(
            f"If you did not create a {brand['app_name']} account, ignore this email "
            "and nothing further will happen."
        )
    )
    return {
        "subject": "Confirm your email address",
        "html": layout(brand, "Verify Email", body),
    }


def welcome(brand: Brand, *, name: str) -> Rendered:
    body = (
        h1(f"Welcome to {brand['app_name']}")
        + p(
            f"Hi {first_name(name)}, your account is live. "
            f"Explore {brand['app_name']} and get started."
        )
        + btn(brand, brand["app_url"], "Open the app")
    )
    return {
        "subject": f"Welcome to {brand['app_name']}",
        "html": layout(brand, "Welcome", body),
    }


def login_notification(
    brand: Brand, *, email: str, ip: str, time: str, user_agent: str
) -> Rendered:
    body = (
        h1("New login to your account")
        + p(f"We recorded a new sign-in to the account registered to {email}.")
        + info_table(
            [
                ("Time", time),
                ("IP Address", ip),
                ("Device", user_agent),
            ]
        )
        + p(
            "Recognise it? Nothing to do. If you do not, reset your password now "
            "and we will end every active session."
        )
        + btn(brand, f"{brand['app_url']}/reset-password", "Reset my password")
        + small("Location is estimated from the IP address and may not be exact.")
    )
    return {
        "subject": "New login to your account",
        "html": layout(brand, "New Login To Your Account", body, recipient_email=email),
    }


def reset_password(brand: Brand, *, email: str, token: str) -> Rendered:
    from urllib.parse import quote

    url = (
        f"{brand['app_url']}/reset-password"
        f"?token={token}&email={quote(email)}"
    )
    body = (
        h1("Reset your password")
        + p(
            f"We received a request to reset the password for {email}. "
            "Set a new one below."
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
        "subject": "Reset your password",
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
    rows = [
        ("Amount", amount),
        ("Listing", listing_title),
    ]
    body = (
        h1("Payment received")
        + p(
            f"Hi {first_name(name)}, your payment was processed successfully "
            f"and your listing is now live on {brand['app_name']}."
        )
        + info_table(rows)
        + btn(brand, brand["app_url"], "View my listing")
    )
    if receipt_url:
        body += p(f'<a href="{receipt_url}" style="color:#1D4ED8;">Download receipt</a>')
    return {
        "subject": f"Payment received — {brand['app_name']}",
        "html": layout(brand, "Payment Received", body),
    }


TEMPLATES: dict[str, Callable[..., Rendered]] = {
    "verify_email": verify_email,
    "welcome": welcome,
    "login_notification": login_notification,
    "reset_password": reset_password,
    "payment_success": payment_success,
}
