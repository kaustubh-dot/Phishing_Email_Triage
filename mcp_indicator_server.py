"""P13's local indicator tools, exposed through the official MCP stdio transport.

The notebook embeds this entire file and recreates it on Run All. No model, data
download, mailbox access or URL fetching is needed to run the server.
The notebook contains the component evaluation.
"""

import html
import re
from email import policy
from email.parser import Parser
from email.utils import getaddresses
from urllib.parse import urlsplit


BRANDS = {
    "paypal.com": "paypal", "microsoft.com": "microsoft",
    "google.com": "google", "amazon.com": "amazon", "apple.com": "apple",
}


def extract_urls(email_text: str) -> list[str]:
    """Extract HTTP(S), www and common defanged URLs locally without fetching them."""
    text = html.unescape(email_text)
    text = re.sub(r"\bhxxp(s?)(?=://)", r"http\1", text, flags=re.I)
    # Normalize spaced scheme/domain spellings only within a URL-shaped span.
    spaced = r"\bhttps?\s*:\s*/\s*/\s*(?:[\w-]+\s*\.\s*)+[\w-]+(?:\s*/[^\s<>]*)?"
    text = re.sub(spaced, lambda match: re.sub(r"\s+", "", match.group()), text, flags=re.I)
    text = text.replace("[.]", ".")
    found = re.findall(r"\b(?:https?://|www\.)[^\s<>\"']+", text, re.I)
    return list(dict.fromkeys(url.rstrip(".,;:!?)]}") for url in found))


def edit_distance(a: str, b: str) -> int:
    row = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        next_row = [i]
        for j, cb in enumerate(b, 1):
            next_row.append(min(next_row[-1] + 1, row[j] + 1, row[j - 1] + (ca != cb)))
        row = next_row
    return row[-1]


def check_domain_lookalike(url: str) -> dict:
    """Flag limited brand lookalikes and deceptive userinfo; no reputation lookup."""
    try:
        parsed = urlsplit(url if "://" in url else "https://" + url)
        host = (parsed.hostname or "").lower().rstrip(".")
        if not host or any(char.isspace() for char in host):
            raise ValueError("missing or invalid host")
        unicode_host = host.encode("ascii").decode("idna") if host.isascii() else host
    except (ValueError, UnicodeError):
        return {"host": "", "flagged": True, "reasons": ["invalid host"], "brand_match": None}
    reasons = []
    if parsed.username is not None:
        reasons.append("URL has user information before the actual destination host")
    for domain in BRANDS:
        if host == domain or host.endswith("." + domain):
            return {"host": host, "flagged": bool(reasons), "reasons": reasons, "brand_match": domain}
    for domain, brand in BRANDS.items():
        if brand in unicode_host:
            reasons.append(f"brand name {brand} outside {domain}")
        for label in unicode_host.split("."):
            folded = label.translate(str.maketrans({"0": "o", "1": "l", "3": "e", "5": "s"}))
            if min(edit_distance(label, brand), edit_distance(folded, brand)) <= 1:
                reasons.append(f"lookalike of {brand}")
    return {"host": host, "flagged": bool(reasons), "reasons": sorted(set(reasons)), "brand_match": None}


def extract_sender_headers(email_text: str) -> dict:
    """Parse claimed sender addresses from leading headers, without authenticating them."""
    message = Parser(policy=policy.default).parsestr(email_text, headersonly=True)
    headers = [str(value) for name in ["from", "sender", "reply-to"]
               for value in message.get_all(name, [])]
    addresses = [address for _, address in getaddresses(headers) if "@" in address]
    return {"sender_addresses": list(dict.fromkeys(addresses)), "sender_headers_present": bool(headers)}


def create_server():
    from mcp.server.fastmcp import FastMCP

    server = FastMCP("P13 email indicators", log_level="WARNING")
    for function in [extract_urls, check_domain_lookalike, extract_sender_headers]:
        server.tool()(function)
    return server


if __name__ == "__main__":
    create_server().run(transport="stdio")
