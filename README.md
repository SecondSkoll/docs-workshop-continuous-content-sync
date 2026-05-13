# DocSync Scout

An AI-powered GitHub Actions workflow that automatically reviews pull requests and evaluates the documentation impact of code changes. When a PR is opened or updated, it analyzes the diff, identifies user-facing changes, scouts for relevant existing documentation pages, and posts a structured report as a PR comment.

## How it works

1. **Trigger** - The workflow fires on PR `opened`, `edited`, and `synchronize` events.
2. **Diff extraction** - The diff between the PR base and head SHAs is captured.
3. **AI analysis** - The diff is passed to the `docs-impact-eval` opencode agent, which runs two skills in sequence:
   - `evaluate-documentation-impact` - determines whether the change affects users (APIs, CLI, config, UI, concepts, or behavioral changes) and produces a structured impact report.
   - `scout-docs` - for each impacted area, scans the `/docs` directory for a matching documentation page by filename first, then by YAML frontmatter metadata (`title`, `tags`, `keywords`, `description`).
4. **PR comment** - The combined impact report and scouting results are posted as a comment on the PR, including the path to any matched pages and instructions for the author.

## Repository structure

```
.github/workflows/opencode-review.yml   # GitHub Actions workflow
.opencode/
  agents/docs-impact-eval.md            # Primary opencode agent
  skills/
    evaluate-documentation-impact/      # Impact analysis skill
    scout-docs/                         # Documentation scouting skill
```

## Requirements

- **`OPENROUTER_API_KEY`** - Set as a repository secret. The agent uses `openrouter/deepseek/deepseek-v4-flash` by default.
- **`GITHUB_TOKEN`** - Automatically provided by GitHub Actions. The workflow requires `pull-requests: write` permission (already configured in the workflow).
- **YAML frontmatter** - For metadata-based scouting to work, documentation pages should include a YAML frontmatter block with at least one of: `title`, `tags`, `keywords`, or `description`. Without frontmatter, `scout-docs` will stop and prompt the author to add metadata.

> **Security note:** Never commit `.env` files or API keys. The `.env` file is excluded via `.gitignore`. If a key is ever exposed, rotate it immediately.

## Setup

1. Copy this repository's `.github/` and `.opencode/` directories into your target repository.
2. Add `OPENROUTER_API_KEY` to your repository's **Settings → Secrets and variables → Actions**.
3. Add YAML frontmatter to your docs pages to enable metadata-based scouting (recommended).

## TODO

- Break down the diff into segments - analysis fails when the diff is too large.
- Add logic to only specific file types in the diff (currently excluded by default).
- Review and continue refining agent and skill prompt files.