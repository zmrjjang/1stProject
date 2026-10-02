"""Best-effort notifications. Every channel is optional and configured by env vars:

  GITHUB_TOKEN + GITHUB_REPOSITORY   -> opens a GitHub issue (repo owner gets an email/app alert)
  NTFY_TOPIC                         -> phone push via https://ntfy.sh (free app, no account)
  TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID
  DISCORD_WEBHOOK_URL
"""

import json
import logging
import os
import urllib.request

log = logging.getLogger("lab")


def _post(url, payload, headers=None):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, method="POST",
                                 headers={"Content-Type": "application/json", **(headers or {})})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.status


def notify(title, message, body_markdown=None, link=None):
    sent = []
    env = os.environ
    channels = [
        ("github", env.get("GITHUB_TOKEN") and env.get("GITHUB_REPOSITORY"), lambda: _post(
            f"https://api.github.com/repos/{env['GITHUB_REPOSITORY']}/issues",
            {"title": title, "body": body_markdown or message},
            {"Authorization": f"Bearer {env['GITHUB_TOKEN']}", "Accept": "application/vnd.github+json"})),
        ("ntfy", env.get("NTFY_TOPIC"), lambda: _post(
            "https://ntfy.sh/", {"topic": env["NTFY_TOPIC"], "title": title, "message": message,
                                 "tags": ["chart_with_upwards_trend"], "priority": 4,
                                 **({"click": link} if link else {})})),
        ("telegram", env.get("TELEGRAM_BOT_TOKEN") and env.get("TELEGRAM_CHAT_ID"), lambda: _post(
            f"https://api.telegram.org/bot{env['TELEGRAM_BOT_TOKEN']}/sendMessage",
            {"chat_id": env["TELEGRAM_CHAT_ID"], "text": f"{title}\n{message}" + (f"\n{link}" if link else "")})),
        ("discord", env.get("DISCORD_WEBHOOK_URL"), lambda: _post(
            env["DISCORD_WEBHOOK_URL"],
            {"content": (f"**{title}**\n{message}" + (f"\n{link}" if link else ""))[:1900]})),
    ]
    for name, enabled, send in channels:
        if not enabled:
            continue
        try:
            send()
            sent.append(name)
        except Exception as e:  # noqa: BLE001 - a failed channel must not stop the search
            log.warning("notify via %s failed: %s", name, e)
    return sent
