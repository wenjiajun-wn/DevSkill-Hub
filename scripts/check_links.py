"""Check local Markdown files and anchors; external links require separate review."""

from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlparse

try:
    from .catalog import ROOT, valid_url
except ImportError:
    from catalog import ROOT, valid_url

EXCLUDED = {".git", ".cache", ".venv", "venv", "node_modules", "__pycache__"}
LINK = re.compile(r"!?\[[^\]\n]*\]\((<[^>]+>|[^\s)]+)(?:\s+\"[^\"]*\")?\)")


def without_code(text):
    return re.sub(r"(?ms)^(```|~~~).*?^\1[^\n]*\n?", "", text)


def anchors(text):
    text = without_code(text)
    result = set(re.findall(r'<a\s+(?:id|name)="([^"]+)"', text))
    counts = {}
    for heading in re.findall(r"(?m)^#{1,6}\s+(.+?)\s*#*\s*$", text):
        heading = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", heading)
        slug = re.sub(r"[^\w\-\s]", "", heading.lower(), flags=re.UNICODE).replace(" ", "-")
        number = counts.get(slug, 0)
        counts[slug] = number + 1
        result.add(slug if number == 0 else f"{slug}-{number}")
    return result


def check_links(root=ROOT):
    root = Path(root).resolve()
    errors, count = [], 0
    for source in root.rglob("*.md"):
        if any(part in EXCLUDED for part in source.relative_to(root).parts):
            continue
        text = without_code(source.read_text(encoding="utf-8"))
        for match in LINK.finditer(text):
            link = match.group(1).strip("<>")
            count += 1
            try:
                parsed = urlparse(link)
            except ValueError:
                errors.append(f"{source.relative_to(root)}: invalid URL {link}")
                continue
            if parsed.scheme or parsed.netloc:
                if not valid_url(link):
                    errors.append(f"{source.relative_to(root)}: external link must use valid HTTPS: {link}")
                continue
            target = (source.parent / unquote(parsed.path)).resolve() if parsed.path else source
            if not target.is_relative_to(root) or not target.is_file():
                errors.append(f"{source.relative_to(root)}: missing or escaping target {link}")
            elif parsed.fragment and target.suffix.lower() == ".md":
                if unquote(parsed.fragment) not in anchors(target.read_text(encoding="utf-8")):
                    errors.append(f"{source.relative_to(root)}: missing anchor {link}")
    return errors, count


def main():
    errors, count = check_links()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Markdown links valid locally ({count} references); external URLs syntax-checked only.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
