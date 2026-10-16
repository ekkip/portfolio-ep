#!/usr/bin/env python3
"""Rewrite root-absolute asset paths for GitHub Pages project sites."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROOT_HTML = {"index.html", "menu.html", "privacy.html"}


def fix_root(content: str) -> str:
    content = content.replace('href="/customStyle.css"', 'href="customStyle.css"')
    content = content.replace('href="/dist/output.css"', 'href="dist/output.css"')
    content = content.replace('href="/index.html"', 'href="index.html"')
    content = content.replace('href="/privacy.html"', 'href="privacy.html"')
    content = content.replace('src="/menu.html"', 'src="menu.html"')
    content = content.replace('href="/projects/', 'href="projects/')
    content = content.replace('src="/img/', 'src="img/')
    content = content.replace("src='/img/", "src='img/")
    # Background URLs land in dist/output.css — paths must be relative to dist/.
    content = re.sub(
        r"bg-\[url\('https://ekkehardpetzold\.de/img/",
        "bg-[url('../img/",
        content,
    )
    content = re.sub(
        r"([a-z]+):bg-\[url\('https://ekkehardpetzold\.de/img/",
        r"\1:bg-[url('../img/",
        content,
    )
    content = re.sub(r"bg-\[url\('/img/", "bg-[url('../img/", content)
    content = re.sub(r"([a-z]+):bg-\[url\('/img/", r"\1:bg-[url('../img/", content)
    content = re.sub(r"bg-\[url\('img/", "bg-[url('../img/", content)
    content = re.sub(r"([a-z]+):bg-\[url\('img/", r"\1:bg-[url('../img/", content)
    return content


def fix_project(content: str) -> str:
    content = content.replace('href="/customStyle.css"', 'href="../customStyle.css"')
    content = content.replace('href="/dist/output.css"', 'href="../dist/output.css"')
    content = content.replace('href="/index.html"', 'href="../index.html"')
    content = content.replace('src="/menu.html"', 'src="../menu.html"')
    content = content.replace('src="/img/', 'src="../img/')
    content = content.replace('src="/video/', 'src="../video/')
    content = re.sub(
        r"bg-\[url\('https://ekkehardpetzold\.de/img/",
        "bg-[url('../img/",
        content,
    )
    content = re.sub(
        r"([a-z]+):bg-\[url\('https://ekkehardpetzold\.de/img/",
        r"\1:bg-[url('../img/",
        content,
    )
    content = re.sub(r"bg-\[url\('/img/", "bg-[url('../img/", content)
    content = re.sub(r"([a-z]+):bg-\[url\('/img/", r"\1:bg-[url('../img/", content)
    return content


def main() -> None:
    for path in sorted(ROOT.rglob("*.html")):
        if "node_modules" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        if path.name in ROOT_HTML:
            updated = fix_root(text)
        elif path.parent.name == "projects":
            updated = fix_project(text)
        else:
            continue
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            print(f"updated {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
