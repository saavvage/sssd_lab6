# PR: Input validation & output encoding

## Problem
User-supplied content was rendered to HTML without encoding; inputs lacked server-side validation (CWE-20/CWE-79).

## Changes
- Centralized validation using a schema (pydantic/joi/validator class).
- Added max length/charset checks; rejected disallowed HTML.
- HTML-encoded output in templates; added Content Security Policy (CSP).
- Extended CI to run SAST and a minimal DAST step (e.g., ZAP baseline).

## How to test
1. Post `<script>alert(1)</script>` to `/comments`; should be stored encoded and render harmlessly.
2. Run `npm test` / `pytest` to see validation unit tests.

Resolves: #<issue-id>
