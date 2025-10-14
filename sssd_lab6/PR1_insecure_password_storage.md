# PR: Fix insecure password storage (bcrypt/argon2)

## Problem
Passwords were hashed with MD5 without a salt (CWE-916/CWE-759).

## Changes
- Migrated to Argon2id (or bcrypt) with per-user salt.
- Implemented lazy-migration: on successful login with legacy hash, rehash and store new hash.
- Added constant-time password comparison.
- Updated docs and added unit tests for hashing & verification.

## How to test
1. Run unit tests: `pytest tests/test_auth.py::test_password_hashing`.
2. Try logging in with an old account; verify that `password_hash_algo=argon2id` after login.
3. Ensure no plaintext or MD5 hashes remain in DB.

## Security
- Hash parameters tuned for target hardware; includes memory cost to deter GPU attacks.
- No behavior regressions; lockout and rate limiting remain in place.

Resolves: #<issue-id>
