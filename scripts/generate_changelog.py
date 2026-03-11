"""Generate root CHANGELOG.md from GitHub Releases.

This script uses the GitHub REST API to fetch releases for the current
repository and writes a Markdown changelog file at the project root.
"""

from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import urllib.error
import urllib.request


REPO = os.environ.get("GITHUB_REPOSITORY", "Tideseed/eptr2")
TOKEN = os.environ.get("GITHUB_TOKEN")
OUTPUT_PATH = Path(__file__).resolve().parents[1] / "CHANGELOG.md"


def _request_json(url: str) -> list[dict]:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "eptr2-changelog-generator",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"

    req = urllib.request.Request(url=url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:  # nosec B310
        payload = resp.read().decode("utf-8")
        return json.loads(payload)


def fetch_all_releases(repo: str) -> list[dict]:
    releases: list[dict] = []
    page = 1
    per_page = 100

    while True:
        url = (
            f"https://api.github.com/repos/{repo}/releases"
            f"?per_page={per_page}&page={page}"
        )
        chunk = _request_json(url)
        if not chunk:
            break

        releases.extend(chunk)
        if len(chunk) < per_page:
            break
        page += 1

    return [r for r in releases if not r.get("draft", False)]


def _format_date(value: str | None) -> str:
    if not value:
        return "unknown-date"
    try:
        # GitHub dates are usually ISO8601 with Z suffix.
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return value
    return dt.astimezone(timezone.utc).date().isoformat()


def render_markdown(repo: str, releases: list[dict]) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Changelog",
        "",
        "All notable changes are published via GitHub Releases.",
        "",
        f"- Repository: [{repo}](https://github.com/{repo})",
        f"- Auto-generated: {now}",
        "",
        "## Releases",
        "",
    ]

    if not releases:
        lines.extend(
            [
                "_No releases found._",
                "",
            ]
        )
        return "\n".join(lines)

    for release in releases:
        tag = release.get("tag_name", "untagged")
        name = release.get("name") or tag
        url = release.get("html_url", f"https://github.com/{repo}/releases")
        date = _format_date(release.get("published_at") or release.get("created_at"))
        prerelease = " (pre-release)" if release.get("prerelease") else ""
        body = (release.get("body") or "").strip()

        lines.append(f"### [{name}]({url}) - {date}{prerelease}")
        lines.append("")
        lines.append(f"- Tag: `{tag}`")
        lines.append("")

        if body:
            lines.append(body)
        else:
            lines.append("_No release notes provided._")

        lines.append("")

    return "\n".join(lines)


def main() -> None:
    try:
        releases = fetch_all_releases(REPO)
    except urllib.error.HTTPError as exc:
        raise SystemExit(f"Failed to fetch releases: HTTP {exc.code}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"Failed to fetch releases: {exc.reason}") from exc

    content = render_markdown(REPO, releases)
    OUTPUT_PATH.write_text(content + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH} with {len(releases)} release(s).")


if __name__ == "__main__":
    main()
