"""Shared catalog loading, validation, sorting, and atomic serialization."""

from datetime import datetime
from pathlib import Path, PurePosixPath
import os
import re
import tempfile
from urllib.parse import urlparse

import yaml

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "catalog" / "skills.yaml"
CATEGORIES = ("frontend", "backend", "database", "engineering")


class CatalogError(ValueError):
    pass


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject silently overwritten YAML keys; preserve dates as ISO strings."""


UniqueKeyLoader.yaml_implicit_resolvers = {
    key: [(tag, rx) for tag, rx in values if tag != "tag:yaml.org,2002:timestamp"]
    for key, values in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


def unique_mapping(loader, node):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node)
        if not isinstance(key, str):
            raise CatalogError("YAML mapping keys must be strings")
        if key in mapping:
            raise CatalogError(f"Duplicate YAML key: {key}")
        mapping[key] = loader.construct_object(value_node)
    return mapping


UniqueKeyLoader.add_constructor("tag:yaml.org,2002:map", unique_mapping)


def load_catalog(path=CATALOG_PATH):
    try:
        return yaml.load(Path(path).read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
    except (OSError, yaml.YAMLError) as exc:
        raise CatalogError(f"Cannot read catalog: {exc}") from exc


def atomic_write(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(text)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def save_catalog(data, path=CATALOG_PATH):
    atomic_write(path, dump_catalog(data))


def dump_catalog(data):
    return yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=100)


def sort_key(skill, repositories):
    stars = repositories[skill["repository"]]["stars"]
    return (CATEGORIES.index(skill["category"]), stars is None,
            -(stars or 0), skill["id"])


def sort_skills(data):
    data["skills"].sort(key=lambda skill: sort_key(skill, data["repositories"]))


def valid_timestamp(value):
    if not isinstance(value, str):
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed.tzinfo is not None
    except ValueError:
        return False


def valid_url(value):
    if not isinstance(value, str):
        return False
    try:
        parsed = urlparse(value)
    except ValueError:
        return False
    return (parsed.scheme == "https" and bool(parsed.hostname)
            and not parsed.username and not parsed.password and not re.search(r"\s", value))


def validate(data):
    """Return actionable errors, including for malformed/untrusted YAML shapes."""
    errors = []
    if not isinstance(data, dict):
        return ["Catalog must be a mapping"]
    if type(data.get("schema_version")) is not int or data["schema_version"] != 1:
        errors.append("schema_version must be 1")
    if not isinstance(data.get("version"), str) or not re.fullmatch(r"\d+\.\d+\.\d+", data["version"]):
        errors.append("version must use MAJOR.MINOR.PATCH")
    categories = data.get("categories")
    if not isinstance(categories, dict) or tuple(categories) != CATEGORIES:
        errors.append(f"categories must be ordered as {', '.join(CATEGORIES)}")
    else:
        for key, labels in categories.items():
            if not isinstance(labels, dict) or any(not isinstance(labels.get(x), str) or not labels[x].strip() for x in ("name", "name_zh")):
                errors.append(f"{key}: category requires name and name_zh")
    repositories, skills = data.get("repositories"), data.get("skills")
    if not isinstance(repositories, dict) or not repositories:
        return errors + ["repositories must be a nonempty mapping"]
    if not isinstance(skills, list) or not skills:
        return errors + ["skills must be a nonempty list"]
    for repo, meta in repositories.items():
        prefix = f"repository {repo}"
        if not isinstance(repo, str) or not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo):
            errors.append(f"{prefix}: invalid owner/repository")
        if not isinstance(meta, dict):
            errors.append(f"{prefix}: must be a mapping")
            continue
        missing = {"url", "default_branch", "stars", "stars_updated_at", "updated_at", "pushed_at", "license", "monitoring"} - meta.keys()
        if missing:
            errors.append(f"{prefix}: missing fields: {', '.join(sorted(missing))}")
            continue
        if meta.get("url") != f"https://github.com/{repo}":
            errors.append(f"{prefix}: URL must match repository")
        stars = meta.get("stars")
        if stars is not None and (type(stars) is not int or stars < 0):
            errors.append(f"{prefix}: stars must be a nonnegative integer or null")
        if (stars is None) != (meta.get("stars_updated_at") is None):
            errors.append(f"{prefix}: stars and stars_updated_at must both be set or both null")
        for field in ("stars_updated_at", "updated_at", "pushed_at"):
            if field not in meta or (meta[field] is not None and not valid_timestamp(meta[field])):
                errors.append(f"{prefix}: {field} must be an ISO timestamp with timezone or null")
        if not isinstance(meta.get("default_branch"), str) or not meta["default_branch"]:
            errors.append(f"{prefix}: default_branch is required")
        monitoring = meta.get("monitoring")
        if (not isinstance(monitoring, dict) or not valid_timestamp(monitoring.get("reviewed_at")) or
                not isinstance(monitoring.get("files"), dict) or not monitoring["files"]):
            errors.append(f"{prefix}: monitoring requires a review timestamp and path/hash baseline")
        else:
            for path, digest in monitoring["files"].items():
                if (not isinstance(path, str) or PurePosixPath(path).is_absolute() or
                        ".." in PurePosixPath(path).parts or "\\" in path or
                        (digest is not None and (not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{40}", digest)))):
                    errors.append(f"{prefix}: invalid monitored path or Git SHA")
        license_info = meta.get("license")
        if not isinstance(license_info, dict):
            errors.append(f"{prefix}: license must be a mapping")
        elif (not valid_url(license_info.get("url")) or
              any(not isinstance(license_info.get(k), str) or not license_info[k].strip() for k in ("spdx", "scope", "note"))):
            errors.append(f"{prefix}: license requires spdx, scope, note and evidence URL")
        elif license_info.get("evidence_status") not in ("declaration-only", "license-file-reviewed"):
            errors.append(f"{prefix}: license evidence_status must distinguish declarations from inspected license files")
    seen = set()
    used_repos = set()
    for index, skill in enumerate(skills):
        if not isinstance(skill, dict):
            errors.append(f"skill #{index + 1}: must be a mapping")
            continue
        prefix = f"skill {skill.get('id', index + 1)}"
        missing = {"id", "name", "category", "description", "description_zh", "repository",
                   "skill_path", "skill_url", "upstream_name", "source_commit", "skill_updated_at",
                   "tags", "use_cases", "use_cases_zh", "install", "verification",
                   "review_notes", "review_notes_zh"} - skill.keys()
        if missing:
            errors.append(f"{prefix}: missing fields: {', '.join(sorted(missing))}")
            continue
        for field in ("id", "name", "description", "description_zh", "repository"):
            if not isinstance(skill.get(field), str) or not skill[field].strip():
                errors.append(f"{prefix}: {field} must be nonempty text")
        skill_id = skill.get("id")
        if not isinstance(skill_id, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", skill_id):
            errors.append(f"{prefix}: invalid ID")
        elif skill_id in seen:
            errors.append(f"{prefix}: duplicate ID")
        else:
            seen.add(skill_id)
        if skill.get("category") not in CATEGORIES:
            errors.append(f"{prefix}: unknown category")
        repo = skill.get("repository")
        if not isinstance(repo, str) or repo not in repositories:
            errors.append(f"{prefix}: unknown repository")
            continue
        used_repos.add(repo)
        if not isinstance(repositories[repo], dict):
            continue
        for field in ("tags", "use_cases", "use_cases_zh"):
            values = skill.get(field)
            if not isinstance(values, list) or not values or any(not isinstance(v, str) or not v.strip() for v in values):
                errors.append(f"{prefix}: {field} must be a nonempty text list")
        path, url = skill.get("skill_path"), skill.get("skill_url")
        if path is not None:
            if not isinstance(path, str) or not path.endswith("/SKILL.md") or "\\" in path or PurePosixPath(path).is_absolute() or ".." in PurePosixPath(path).parts:
                errors.append(f"{prefix}: unsafe or invalid skill_path")
            expected = f"https://github.com/{repo}/blob/{repositories[repo].get('default_branch')}/{path}"
            if url != expected:
                errors.append(f"{prefix}: skill_url must match repository, branch and path")
        elif url is not None:
            errors.append(f"{prefix}: skill_url requires skill_path")
        verification, install = skill.get("verification"), skill.get("install")
        if not isinstance(verification, dict) or not isinstance(install, dict):
            errors.append(f"{prefix}: verification and install must be mappings")
            continue
        missing = {"metadata", "installation", "installation_tested", "effectiveness", "last_reviewed", "test_report_url", "installation_test_report_url", "smoke_scope", "smoke_report_url"} - verification.keys()
        missing_install = {"command", "documentation_url", "notes", "notes_zh"} - install.keys()
        if missing or missing_install:
            errors.append(f"{prefix}: missing verification or install fields")
            continue
        for flag in ("metadata", "installation", "installation_tested", "effectiveness"):
            if type(verification.get(flag)) is not bool:
                errors.append(f"{prefix}: verification.{flag} must be boolean")
        reviewed = verification.get("last_reviewed")
        if reviewed is not None and not valid_timestamp(reviewed):
            errors.append(f"{prefix}: invalid last_reviewed")
        if verification.get("metadata"):
            commit = skill.get("source_commit")
            if (not isinstance(path, str) or not isinstance(skill.get("upstream_name"), str) or
                    not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40}", commit) or
                    not valid_timestamp(skill.get("skill_updated_at")) or not valid_timestamp(reviewed)):
                errors.append(f"{prefix}: metadata verification requires path, upstream_name, commit and review/update timestamps")
        command = install.get("command")
        if command is not None and (not isinstance(command, str) or not command.strip()):
            errors.append(f"{prefix}: install.command must be nonempty text or null")
        if verification.get("installation") and (not command or not valid_url(install.get("documentation_url"))):
            errors.append(f"{prefix}: installation verification requires command and documentation URL")
        if command and not verification.get("installation"):
            errors.append(f"{prefix}: unverified command must be null")
        if verification.get("installation_tested") and (not verification.get("installation") or not valid_url(verification.get("installation_test_report_url"))):
            errors.append(f"{prefix}: installation test claim requires reviewed instructions and installation_test_report_url")
        if verification.get("effectiveness") and not valid_url(verification.get("test_report_url")):
            errors.append(f"{prefix}: effectiveness claim requires test report URL")
        if verification.get("smoke_scope") not in ("not-tested", "tool-smoke", "manual-walkthrough"):
            errors.append(f"{prefix}: invalid smoke_scope")
        if verification.get("smoke_scope") != "not-tested" and not valid_url(verification.get("smoke_report_url")):
            errors.append(f"{prefix}: smoke evidence requires smoke_report_url")
        for field in ("notes", "notes_zh"):
            if not isinstance(install.get(field), str):
                errors.append(f"{prefix}: install.{field} must be text")
        for field in ("review_notes", "review_notes_zh"):
            if not isinstance(skill.get(field), str):
                errors.append(f"{prefix}: {field} must be text")
    if used_repos != set(repositories):
        errors.append("Every repository must be referenced by a skill")
    if not errors and skills != sorted(skills, key=lambda skill: sort_key(skill, repositories)):
        errors.append("Skills must be grouped by category and sorted by repository stars descending (null last, ID tie-break)")
    return errors
