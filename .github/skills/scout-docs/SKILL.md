---
name: scout-docs
description: Identifies relevant documentation pages via filename and metadata analysis.
version: 1.0.0
tools:
  - name: git_api_fetcher
    description: Fetches file content and trees from the repository.
---

# scout-docs

Your goal is to locate the most relevant existing documentation page for a given feature name by inspecting filenames and YAML metadata in the `/docs` directory.

## When to Use This Skill

Use this skill when:
- A user asks to find documentation for a feature
- You need to check whether a doc page already exists before creating a new one
- A code change has been identified and you need to locate the page to update
- Keywords: find docs, scout documentation, locate page, existing documentation, feature docs

## Requirements

- Must scan filenames before inspecting metadata
- Must stop and prompt the user if a filename match is found — do not continue to metadata
- Must check for a `---` YAML header before attempting to parse metadata
- Should match against `title`, `tags`, `keywords`, and `description` metadata keys
- Avoid creating a new page if a match already exists
- Avoid parsing metadata if no files contain a `---` header — return the metadata wall message and terminate

## Execution Logic

1. **Filename Scan**: Search the `/docs` directory for any `.md` file whose name contains the `feature_name`. If found, stop and prompt the user to update that page.
2. **Metadata Verification**: If no filename match is found, inspect the first 10 lines of each file for a `---` YAML header.
3. **The "Metadata Wall"**: If **no files** contain a `---` YAML header, return the following message and **TERMINATE**:
   > "STOP: No metadata found in documentation pages. Add metadata to enable scouting."
4. **Targeted Search**: If metadata exists, parse the keys (e.g., `title`, `tags`, `keywords`, `description`) for the `feature_name`.

## Inputs

- `feature_name`: (String) The core feature/functionality to search for.
- `inventory`: (List) A list of file paths from the Git Tree API.

## Outputs

- `match`: The path to the relevant file.
- `status`: `"match_found"`, `"new_page_required"`, or `"metadata_missing_stop"`.
- `message`: A human-readable explanation of the result.

## References

- Core logic implementation: [scout-logic.py](scout-logic.py)

## Examples

### Good Example — Filename match

**Input**: `feature_name = "testing"`, inventory contains `docs/testing.md`

**Output**:
```json
{
  "status": "match_found",
  "path": "docs/testing.md",
  "reason": "Filename match",
  "message": "A documentation page on this topic already exists at 'docs/testing.md'. Consider updating it to reflect your new change."
}
```

### Good Example — Metadata match

**Input**: `feature_name = "testing"`, inventory contains `docs/run.md` with description `"This page explains the user how to test."`

**Output**:
```json
{
  "status": "match_found",
  "path": "docs/run.md",
  "reason": "Metadata match",
  "message": "A documentation page on this topic already exists at 'docs/run.md'. Consider updating it to reflect your new change."
}
```

### What to Avoid

- Do **not** proceed to metadata scanning if a filename match was already found.
- Do **not** attempt to parse YAML if no `---` header is present — trigger the metadata wall instead.
- Do **not** create a new page without first completing both the filename and metadata scan.