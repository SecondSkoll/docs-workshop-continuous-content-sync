# DocSync Scout

This repository contains an initial framework to leverage AI in understanding the impact of a code change on documentation.

## Outline

This repository uses an opencode based workflow that triggers on a PR. It examines the diff of a PR (or any manual diff), and explores the impact of any changes. It then provides a comment on the changes and provides advice in a comment on the PR.

# Requirements

OpenCode Agents installed on your GitHub repo (otherwise comment functionality does not work).

`OPENROUTER_API_KEY` set in your GitHub repo's secrets.

# TODO

- Break down the diff into segments, as it fails when the diff is too large.
- Add logic to handle python inclusion (add to diff command)
- Revise model use - Deepseek Pro proved to be more effective
- Review and continue refining agent and skill files