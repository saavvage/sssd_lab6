# PR: Prevent SQL Injection in search endpoint

## Problem
The `/search` endpoint built SQL via string concatenation (CWE-89).

## Changes
- Switched to parameterized queries with placeholders.
- Escaped LIKE wildcards (`%` and `_`) safely.
- Restricted page size and added allowlist for sortable fields.
- Added unit tests that attempt common payloads and expect no results rather than errors.

## How to test
1. `pytest tests/test_search.py`
2. Manual: `GET /search?q=%27%20OR%201=1--` should return 400 or empty results.

Resolves: #<issue-id>
