import re
from pathlib import Path

SECRET_PATTERNS = [re.compile(r"AKIA[0-9A-Z]{16}"), re.compile(r"(?i)(api_key|secret|token|password)\s*=\s*['\"][^'\"]+['\"]")]

def scan_text(text):
    return [pat.pattern for pat in SECRET_PATTERNS if pat.search(text)]

def scan_path(path):
    findings = []
    for file in Path(path).rglob("*"):
        if file.is_file() and file.suffix.lower() in {".py", ".md", ".yaml", ".yml", ".txt", ".json"}:
            matches = scan_text(file.read_text(encoding="utf-8", errors="ignore"))
            if matches:
                findings.append({"file": str(file), "patterns": matches})
    return {"status": "PASS" if not findings else "FAIL", "findings": findings}

