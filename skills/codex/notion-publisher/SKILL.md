---
name: notion-publisher
description: Publish or update polished Notion pages from Markdown, drafts, local files, or structured content. Use when the user asks to write, publish, upload, or sync content into Notion.
metadata:
  short-description: Publish drafts and Markdown into Notion
---

# Notion Publisher

Use this skill to publish content into Notion through the Notion MCP connection.

## Workflow

1. Determine the target parent page or database. Default to `听风楼·问道手札` when the user does not specify.
2. If the user provides a local file, read it and preserve Markdown structure.
3. Search Notion for an existing page with the same title.
4. Ask before overwriting a substantial existing page unless the user explicitly requested an update.
5. Create or update the Notion page.
6. Return the Notion page URL and a short summary of what was published.

## Publishing Guidelines

- Preserve headings, lists, code blocks, tables where supported, and links.
- Use compact, readable page titles.
- For long documents, add a short summary at the top.
- Do not publish secrets or credentials into Notion. Store secrets in 1Password and publish only references.

## Example Requests

- "Publish this Markdown file to Notion under 听风楼·问道手札."
- "Create a Notion page from these notes."
- "Update the existing Notion page with this release note."
