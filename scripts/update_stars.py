"""Refresh repository stars once per repository; never write an incomplete refresh."""

import argparse
from copy import deepcopy
from datetime import datetime, timezone
from http.client import HTTPException
import json
import os
from pathlib import Path
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

try:
    from .catalog import CATALOG_PATH, CatalogError, dump_catalog, load_catalog, sort_skills, validate
    from .render_catalog import render_all
    from .transaction import commit_files, write_lock
except ImportError:
    from catalog import CATALOG_PATH, CatalogError, dump_catalog, load_catalog, sort_skills, validate
    from render_catalog import render_all
    from transaction import commit_files, write_lock


class GitHubError(RuntimeError):
    """A sanitized API error, safe to print without request credentials."""


def fetch_repository(repository, token=None, opener=urlopen, sleeper=time.sleep):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "DevSkill-Hub/0.1.0",
               "X-GitHub-Api-Version": "2022-11-28"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(f"https://api.github.com/repos/{repository}", headers=headers)
    for attempt in range(3):
        try:
            with opener(request, timeout=20) as response:
                data = json.load(response)
            if not isinstance(data, dict) or type(data.get("stargazers_count")) is not int or data["stargazers_count"] < 0:
                raise GitHubError(f"{repository}: invalid stargazers_count in API response")
            # Refresh counters only. Upstream path/license/content changes need human review.
            return data["stargazers_count"]
        except HTTPError as exc:
            if exc.code in (403, 429):
                reset = exc.headers.get("X-RateLimit-Reset", "unknown") if exc.headers else "unknown"
                retry = exc.headers.get("Retry-After", "unknown") if exc.headers else "unknown"
                raise GitHubError(f"{repository}: HTTP {exc.code}; access denied or rate limited (reset epoch: {reset}; retry-after: {retry}). Retry later or use GH_TOKEN/GITHUB_TOKEN.") from None
            if exc.code == 404:
                raise GitHubError(f"{repository}: repository not found (HTTP 404); review catalog manually") from None
            if exc.code in (500, 502, 503, 504) and attempt < 2:
                sleeper(2 ** attempt)
                continue
            raise GitHubError(f"{repository}: GitHub returned HTTP {exc.code}") from None
        except (URLError, TimeoutError, OSError, HTTPException):
            if attempt < 2:
                sleeper(2 ** attempt)
                continue
            raise GitHubError(f"{repository}: network request failed after 3 attempts") from None
        except (ValueError, UnicodeError):
            raise GitHubError(f"{repository}: invalid JSON in API response") from None


def refresh(data, fetcher, timestamp):
    """Gather all results before modifying a copy; failures preserve previous data."""
    repositories = list(dict.fromkeys(skill["repository"] for skill in data["skills"]))
    stars = {repository: fetcher(repository) for repository in repositories}
    updated = deepcopy(data)
    for repository, count in stars.items():
        if type(count) is not int or count < 0:
            raise GitHubError(f"{repository}: invalid star count")
        updated["repositories"][repository]["stars"] = count
        updated["repositories"][repository]["stars_updated_at"] = timestamp
    sort_skills(updated)
    return updated


def run(args):
    data = load_catalog(args.catalog)
    errors = validate(data)
    if errors:
        raise CatalogError("; ".join(errors))
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    updated = refresh(data, lambda repo: fetch_repository(repo, token),
                      datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"))
    completed_at = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    for repository in updated["repositories"].values():
        repository["stars_updated_at"] = completed_at
    for repo, meta in updated["repositories"].items():
        print(f"{repo}: {meta['stars']:,}")
    root = Path(args.catalog).resolve().parent.parent
    outputs = render_all(updated, root=root)
    if args.dry_run:
        print("Dry run: no project files changed.")
        return 0
    outputs[Path(args.catalog).resolve()] = dump_catalog(updated)
    commit_files(outputs, root)
    print("Stars, sorting, and generated documentation updated.")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", default=CATALOG_PATH)
    parser.add_argument("--dry-run", action="store_true", help="Fetch and report without changing files")
    args = parser.parse_args(argv)
    try:
        with write_lock(Path(args.catalog).resolve().parent.parent):
            return run(args)
    except (CatalogError, GitHubError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
