"""Validate catalog structure, evidence, URLs, and ordering without network access."""

import argparse
import sys

try:
    from .catalog import CATALOG_PATH, CatalogError, load_catalog, validate
except ImportError:
    from catalog import CATALOG_PATH, CatalogError, load_catalog, validate


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", default=CATALOG_PATH)
    args = parser.parse_args(argv)
    try:
        data = load_catalog(args.catalog)
        errors = validate(data)
    except CatalogError as exc:
        errors = [str(exc)]
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Catalog valid: {len(data['skills'])} skills, {len(data['repositories'])} repositories.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
