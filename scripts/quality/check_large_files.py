import sys
from pathlib import Path
limit = 25 * 1024 * 1024
bad = [p for p in Path(sys.argv[1] if len(sys.argv) > 1 else ".").rglob("*") if p.is_file() and ".git" not in p.parts and p.stat().st_size > limit]
for p in bad:
    print(p)
raise SystemExit(1 if bad else 0)

