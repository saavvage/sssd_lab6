# Security Code Review Checklist (quick)

- [ ] Auth & session: strong hashing (Argon2/bcrypt), TLS, anti-bruteforce, secure cookies, CSRF.
- [ ] Access control: endpoints enforce authorization server-side; no IDOR; deny-by-default.
- [ ] Input handling: validate, sanitize, and encode. Prefer parameterized DB queries everywhere.
- [ ] Cryptography: no custom crypto; modern algorithms; unique salts; keys not in repo.
- [ ] Secrets: .env or secret manager; rotate leaked keys; add secret scanning in CI.
- [ ] Error handling & logging: no stack traces to users; central logging with correlation IDs.
- [ ] Dependencies: pinned versions, audits in CI, remove abandoned libs.
- [ ] Build/CI: SAST, dependency scan, secret scan, tests required for merge, CODEOWNERS.
- [ ] Infrastructure: least privilege for DB/users/tokens; principle of least privilege everywhere.
- [ ] Documentation: threat model notes, data flow, and risk ratings recorded in REPORT.
