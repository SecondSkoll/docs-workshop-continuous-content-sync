---
name: evaluate-documentation-impact
description: "Evaluate the impact of code changes on documentation"
---

# evaluate-documentation-impact

## Description

This skill analyzes a codebase change to determine its impact on end-users.
It helps documentation writers understand exactly which parts of the documentation require updates.

## 1. Analyze

Scan the `git diff` to understand the changes. Determine if the changes will have an impact on users.
Consider whether the changes will have an impact on any of the following:

- Public APIs
- CLI
- Configuration settings
- User interface
- Behavioral changes
- Important concepts

## 2. Evaluate

Determine whether the changes will have an impact on users or not:

- **No impact**: Refactors, internal logic optimizations, or test updates that do not change how a user interacts with the software.
- **Impact**: Changes that will impact how a user will interact with the software.

## 3. Explain

If the changes will have an impact on users, then:

- **Identify**: Explain who will be effected. (For example: "Developers using the REST API", "End-users of the UI dashboard", etc.)
- **Describe**: Explain what changed in plain language.

## 4. Output format

Structure the output as a report formatted in Markdown:

---
# User impact assessment

**Impact detected**: [Yes/No]

## Analysis summary

Provide a 2--3 sentence overview of what the diff represents.

## Impacted areas

- **Category**: (e.g., API, UI, configuration, concept)
- **Change**: (Brief description)
- **User explanation**: (How this affects the user)
---

