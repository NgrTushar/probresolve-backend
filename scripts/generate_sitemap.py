"""
Generate sitemap.xml for ProbResolve.

Usage:
    python scripts/generate_sitemap.py

Writes sitemap.xml to the project root.
Run manually or via cron after new content is published.
"""

import asyncio
import sys
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, indent, tostring

from sqlalchemy import select

# Allow running from project root
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import async_engine  # noqa: E402
from app.models import Domain, Problem  # noqa: E402

BASE_URL = "https://probresolve.com"
OUTPUT = Path(__file__).parent.parent / "sitemap.xml"


async def generate() -> None:
    urlset = Element("urlset")
    urlset.set("xmlns", "https://www.sitemaps.org/schemas/sitemap/0.9")

    def add_url(loc: str, lastmod: str | None = None, changefreq: str = "weekly", priority: str = "0.5") -> None:
        url = SubElement(urlset, "url")
        SubElement(url, "loc").text = loc
        if lastmod:
            SubElement(url, "lastmod").text = lastmod
        SubElement(url, "changefreq").text = changefreq
        SubElement(url, "priority").text = priority

    # Static pages
    add_url(BASE_URL + "/", changefreq="daily", priority="1.0")
    add_url(BASE_URL + "/problems/new", changefreq="monthly", priority="0.3")

    async with async_engine.connect() as conn:
        # Domain filter pages
        rows = await conn.execute(select(Domain.id, Domain.slug))
        for domain_id, domain_slug in rows:
            add_url(f"{BASE_URL}/?domain_id={domain_id}", changefreq="daily", priority="0.8")

        # Individual problem pages
        rows = await conn.execute(
            select(Problem.id, Problem.slug, Problem.updated_at).order_by(Problem.created_at.desc())
        )
        for problem_id, problem_slug, updated_at in rows:
            lastmod = updated_at.strftime("%Y-%m-%d") if updated_at else None
            add_url(
                f"{BASE_URL}/problems/{problem_id}/{problem_slug}",
                lastmod=lastmod,
                changefreq="weekly",
                priority="0.6",
            )

    await async_engine.dispose()

    indent(urlset, space="  ")
    xml_bytes = b'<?xml version="1.0" encoding="UTF-8"?>\n' + tostring(urlset, encoding="unicode").encode()
    OUTPUT.write_bytes(xml_bytes)
    print(f"sitemap.xml written to {OUTPUT} ({OUTPUT.stat().st_size} bytes)")


if __name__ == "__main__":
    asyncio.run(generate())
