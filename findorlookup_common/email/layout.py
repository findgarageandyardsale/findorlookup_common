from typing import Iterable, Tuple

from findorlookup_common.settings.brand import Brand


SANS = "-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif"
SERIF = "Georgia,'Times New Roman',serif"


def first_name(name: str) -> str:
    return (name or "").split(" ")[0]


def layout(brand: Brand, label: str, body: str, recipient_email: str = "") -> str:
    logo = brand.get("logo_url") or ""
    support = brand["support_email"]
    app_name = brand["app_name"]
    primary = brand.get("primary_color") or "#111827"
    header_left = (
        f'<img src="{logo}" alt="{app_name}" height="44" '
        f'style="display:block;height:44px;width:auto;border:0;"/>'
        if logo
        else (
            f'<span style="font-size:18px;font-weight:700;color:{primary};'
            f'letter-spacing:-0.2px;font-family:Georgia,serif;">{app_name}</span>'
        )
    )
    security_note = (
        f'<p style="margin:0;font-size:12px;color:#9CA3AF;line-height:1.6;font-family:{SANS};">'
        f"Security notice sent to {recipient_email}. Account-security messages cannot be turned off.</p>"
        if recipient_email
        else ""
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/></head>
<body style="margin:0;padding:0;background-color:#ECEAE3;font-family:{SANS};">
<table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#ECEAE3;">
  <tr><td align="center" style="padding:40px 16px;">
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width:560px;background-color:#FFFFFF;">
      <tr><td style="padding:28px 32px 20px;">
        <table width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
          <td>{header_left}</td>
          <td align="right" valign="middle"><span style="font-size:10px;font-weight:700;color:#9CA3AF;letter-spacing:1.5px;text-transform:uppercase;font-family:{SANS};">{label}</span></td>
        </tr></table>
      </td></tr>
      <tr><td style="padding:0 32px;">
        <table width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
          <td width="33%" height="3" style="background-color:#16A34A;font-size:0;line-height:0;">&nbsp;</td>
          <td width="33%" height="3" style="background-color:#DC2626;font-size:0;line-height:0;">&nbsp;</td>
          <td width="34%" height="3" style="background-color:#1D4ED8;font-size:0;line-height:0;">&nbsp;</td>
        </tr></table>
      </td></tr>
      <tr><td style="padding:32px 32px 8px;">{body}</td></tr>
      <tr><td style="padding:20px 32px 32px;border-top:1px solid #E5E7EB;">
        <p style="margin:0 0 3px;font-size:12px;color:#6B7280;line-height:1.6;font-family:{SANS};">
          <strong style="color:#374151;">{app_name}</strong> &middot; A FindOrLookup app.
        </p>
        <p style="margin:0 0 3px;font-size:12px;color:#6B7280;line-height:1.6;font-family:{SANS};">
          Questions? Reach us at <a href="mailto:{support}" style="color:#1D4ED8;text-decoration:none;">{support}</a>.
        </p>
        {security_note}
      </td></tr>
    </table>
  </td></tr>
</table>
</body></html>"""


def h1(text: str) -> str:
    return (
        f'<h1 style="margin:0 0 16px;font-size:24px;font-weight:700;color:#111827;'
        f'line-height:1.2;font-family:{SERIF};">{text}</h1>'
    )


def p(text: str) -> str:
    return (
        f'<p style="margin:0 0 16px;font-size:15px;color:#374151;line-height:1.6;'
        f'font-family:{SANS};">{text}</p>'
    )


def small(text: str) -> str:
    return (
        f'<p style="margin:20px 0 0;font-size:13px;color:#6B7280;line-height:1.6;'
        f'font-family:{SANS};">{text}</p>'
    )


def btn(brand: Brand, href: str, label: str, color: str | None = None) -> str:
    bg = color or brand["primary_color"]
    return (
        f'<table cellpadding="0" cellspacing="0" border="0" style="margin:24px 0 8px;"><tr>'
        f'<td style="background-color:{bg};border-radius:3px;">'
        f'<a href="{href}" style="display:inline-block;padding:13px 28px;font-size:14px;'
        f'font-weight:600;color:#FFFFFF;text-decoration:none;font-family:{SANS};">{label}</a>'
        f"</td></tr></table>"
    )


def step(brand: Brand, num: int, title: str, body: str, color: str | None = None) -> str:
    bg = color or brand["primary_color"]
    return (
        f'<table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:20px;"><tr>'
        f'<td valign="top" width="36" style="padding-right:14px;padding-top:1px;">'
        f'<span style="display:inline-block;width:26px;height:26px;background-color:{bg};'
        f'border-radius:50%;font-size:13px;font-weight:700;color:#FFFFFF;text-align:center;'
        f'line-height:26px;font-family:{SANS};">{num}</span></td>'
        f'<td valign="top">'
        f'<p style="margin:0 0 4px;font-size:14px;font-weight:600;color:#111827;font-family:{SANS};">{title}</p>'
        f'<p style="margin:0;font-size:13px;color:#6B7280;line-height:1.5;font-family:{SANS};">{body}</p>'
        f"</td></tr></table>"
    )


def info_table(rows: Iterable[Tuple[str, str]]) -> str:
    cells = "".join(
        f"""
    <tr>
      <td style="padding:10px 0;border-bottom:1px solid #E5E7EB;">
        <span style="font-size:11px;font-weight:700;color:#9CA3AF;letter-spacing:1px;text-transform:uppercase;font-family:{SANS};">{label}</span>
      </td>
      <td style="padding:10px 0;border-bottom:1px solid #E5E7EB;text-align:right;">
        <span style="font-size:13px;color:#111827;font-family:{SANS};">{value}</span>
      </td>
    </tr>"""
        for label, value in rows
    )
    return (
        f'<table width="100%" cellpadding="0" cellspacing="0" border="0" '
        f'style="border-top:1px solid #E5E7EB;margin:20px 0;">{cells}</table>'
    )


def warning_box(text: str) -> str:
    return (
        f'<table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:20px 0;"><tr>'
        f'<td style="padding:14px 16px;border-left:4px solid #FCA5A5;background-color:#FEF2F2;">'
        f'<p style="margin:0;font-size:13px;color:#374151;line-height:1.5;font-family:{SANS};">{text}</p>'
        f"</td></tr></table>"
    )


def fallback(url: str, expiry: str) -> str:
    return (
        f'<p style="margin:20px 0 0;font-size:13px;color:#6B7280;line-height:1.6;font-family:{SANS};">'
        f"This link expires in {expiry}. If the button does not work, paste this address into your browser:<br/>"
        f'<a href="{url}" style="color:#1D4ED8;font-size:12px;word-break:break-all;">{url}</a>'
        f"</p>"
    )
