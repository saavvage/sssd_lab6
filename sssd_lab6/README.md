# Lab 6 — Security Code Review (Flask + SQLite)

This repo intentionally starts **with vulnerabilities** so you can open Issues and PRs.

## Endpoints
- `POST /register` with form fields `username`, `password`
- `POST /login` with form fields `username`, `password`
- `GET /search?q=<term>`
- `GET /comments` (list), `POST /comments` (add via form)

## Quick start
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=app.py
python init_db.py
flask run
```

## Security tasks & branches
You will create three branches and PRs:

1. `fix/hash` — replace MD5 with Argon2id (lazy migration), update tests.
2. `fix/sql` — parameterize SQL and escape LIKE wildcards.
3. `fix/validation` — input validation, HTML-encoding, add CSP header.

Patches for each PR are provided in `patches/`. After creating a branch, apply the corresponding patch:
```bash
git checkout -b fix/hash
git apply patches/0001-security-replace-md5-with-argon2.patch
git add -A && git commit -m "security: replace md5 with argon2 (CWE-916)"
git push origin fix/hash
# open PR using template PR1_insecure_password_storage.md
```

### Tests (will FAIL before fixes)
```bash
pytest -q
```

Run them again after merging each PR — they should pass when all fixes are applied.
