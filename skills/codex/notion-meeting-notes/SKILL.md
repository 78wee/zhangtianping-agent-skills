---
name: notion-meeting-notes
description: Create, clean up, or publish meeting notes in Notion. Use when the user asks to turn a transcript, call notes, agenda, decisions, or action items into a Notion meeting note.
metadata:
  short-description: Turn meetings and transcripts into Notion notes
---

# Notion Meeting Notes

Use this skill to turn meeting material into structured Notion pages.

## Workflow

1. Confirm the target parent page or database. Default to the user's Hermes/Notion root page if available: `听风楼·问道手札`.
2. Extract:
   - Meeting title
   - Date
   - Attendees, if provided
   - Summary
   - Decisions
   - Action items with owners and due dates, if provided
   - Open questions
3. Search Notion for an existing related meeting page before creating duplicates.
4. Create or update a Notion page using the Notion MCP tools.
5. Link related pages when possible.

## Suggested Page Template

```markdown
# [Meeting Title]

## Summary

## Decisions

## Action Items

## Open Questions

## Raw Notes / Transcript
```

## Notes

- Do not store secrets in meeting notes unless the user explicitly asks and the target page is appropriate.
- Prefer concise summaries over verbatim transcripts unless the user requests full archival.
