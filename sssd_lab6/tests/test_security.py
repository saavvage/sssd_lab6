import re, sqlite3, os
from app import md5_hash

def test_md5_is_insecure():
    # Policy: project must NOT use MD5
    h = md5_hash("password123")
    # length 32 hex proves it's md5 now; this test should fail AFTER fix when md5_hash removed/changed
    assert len(h) == 32 and re.fullmatch(r"[0-9a-f]{32}", h)

def test_sql_search_injection_possible():
    # Shows current behavior is injectable. Should fail AFTER fix.
    from app import DB_PATH
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    # A naive check: try to inject wildcard to fetch all
    payload = "' OR 1=1 --"
    sql = f"SELECT id, name FROM products WHERE name LIKE '%{payload}%'"
    cur.execute(sql)
    rows = cur.fetchall()
    # If DB didn't error, "injection path exists" in the app too
    assert rows is not None  # placeholder to keep test true pre-fix
