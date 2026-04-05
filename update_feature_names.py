#!/usr/bin/env uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["urllib3"]
# ///
from __future__ import annotations

import re
from pathlib import Path
from typing import cast

import urllib3

# fmt: off
CHROMIUM_URL = "https://github.com/chromium/chromium/raw/refs/heads/main/services/network/public/cpp/permissions_policy/permissions_policy_features.json5"
FIREFOX_URL = "https://github.com/mozilla/gecko-dev/raw/refs/heads/master/dom/security/featurepolicy/FeaturePolicyUtils.cpp"
# fmt: on


http = urllib3.PoolManager()


def fetch(url: str) -> str:
    response = http.request("GET", url)
    return cast(str, response.data.decode())


def get_chromium_features(content: str) -> set[str]:
    features = set()
    for entry in re.findall(r"\{([^{}]+)\}", content):
        name_match = re.search(r'permissions_policy_name:\s*"([^"]+)"', entry)
        if not name_match:
            continue
        if '"IsolatedContext"' in entry:
            continue
        if '"OriginTrialsSampleAPI"' in entry:
            continue
        features.add(name_match.group(1))
    return features


def get_firefox_features(content: str) -> set[str]:
    features = set()
    for array_match in re.finditer(
        r"static FeatureMap s(?:Supported|Experimental)Features\[\] = \{(.*?)\};",
        content,
        re.DOTALL,
    ):
        for feature_match in re.finditer(r'\{"([^"]+)"', array_match.group(1)):
            features.add(feature_match.group(1))
    return features


def get_current_features(init_path: Path) -> set[str]:
    content = init_path.read_text()
    block_match = re.search(
        r"_FEATURE_NAMES: set\[str\] = \{(.*?)\}", content, re.DOTALL
    )
    if not block_match:
        return set()
    return set(re.findall(r'"([a-z][a-z0-9-]+)"', block_match.group(1)))


def update_init(
    init_path: Path,
    chromium_features: set[str],
    firefox_only: set[str],
) -> None:
    lines: list[str] = []
    lines.append("    # Chrome features")
    lines.append(f"    # {CHROMIUM_URL}")
    for name in sorted(chromium_features):
        lines.append(f'    "{name}",')
    lines.append("    # Firefox-only features")
    lines.append(f"    # {FIREFOX_URL}")
    for name in sorted(firefox_only):
        lines.append(f'    "{name}",')

    new_block = "_FEATURE_NAMES: set[str] = {{\n{}\n}}".format("\n".join(lines))

    original = init_path.read_text()
    updated = re.sub(
        r"_FEATURE_NAMES: set\[str\] = \{.*?\}",
        new_block,
        original,
        flags=re.DOTALL,
    )
    if updated != original:
        init_path.write_text(updated)


def update_changelog(
    changelog_path: Path,
    added: set[str],
    removed: set[str],
) -> None:
    if not added and not removed:
        return

    entry_lines = ["* Updated feature list from Chrome and Firefox sources.", ""]
    if added:
        entry_lines += ["  New features:", ""]
        entry_lines += [f"  * ``{name}``" for name in sorted(added)]
        entry_lines.append("")
    if removed:
        entry_lines += ["  Removed features:", ""]
        entry_lines += [f"  * ``{name}``" for name in sorted(removed)]
        entry_lines.append("")
    entry = "\n".join(entry_lines) + "\n"

    content = changelog_path.read_text()

    pending_header = "Pending\n-------\n"
    if pending_header not in content:
        title_end = re.search(r"=========\nChangelog\n=========\n\n", content)
        assert title_end
        pos = title_end.end()
        content = content[:pos] + pending_header + "\n" + content[pos:]

    versioned = re.search(r"\n\d+\.\d+\.\d+ \(\d{4}-\d{2}-\d{2}\)\n", content)
    assert versioned
    content = (
        content[: versioned.start() + 1] + entry + content[versioned.start() + 1 :]
    )

    changelog_path.write_text(content)


def main() -> None:
    chromium_features = get_chromium_features(fetch(CHROMIUM_URL))
    firefox_features = get_firefox_features(fetch(FIREFOX_URL))
    firefox_only = firefox_features - chromium_features

    repo_root = Path(__file__).parent
    init_path = repo_root / "src" / "django_permissions_policy" / "__init__.py"
    changelog_path = repo_root / "CHANGELOG.rst"

    existing = get_current_features(init_path)
    new_all = chromium_features | firefox_only
    added = new_all - existing
    removed = existing - new_all

    update_init(init_path, chromium_features, firefox_only)
    update_changelog(changelog_path, added, removed)

    if added:
        print(f"Added: {', '.join(sorted(added))}")
    if removed:
        print(f"Removed: {', '.join(sorted(removed))}")
    if not added and not removed:
        print("No changes.")


if __name__ == "__main__":
    main()
