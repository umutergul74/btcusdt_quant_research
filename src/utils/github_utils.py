import os
import re
import subprocess
from typing import List, Dict

def scan_for_secrets(project_root: str) -> Dict[str, List[str]]:
    """Scans files under project_root for potential secrets, ignoring excluded patterns."""
    secrets_found = {}
    secret_patterns = [
        re.compile(r"api[_-]?key\s*=\s*['\"][a-zA-Z0-9_\-]{10,}['\"]", re.IGNORECASE),
        re.compile(r"secret\s*=\s*['\"][a-zA-Z0-9_\-]{10,}['\"]", re.IGNORECASE),
        re.compile(r"token\s*=\s*['\"][a-zA-Z0-9_\-]{10,}['\"]", re.IGNORECASE),
        re.compile(r"password\s*=\s*['\"][a-zA-Z0-9_\-]{6,}['\"]", re.IGNORECASE)
    ]
    
    # Excluded directories
    exclude_dirs = {".git", ".ipynb_checkpoints", "data", "models", "logs", "cache"}
    
    for root, dirs, files in os.walk(project_root):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            if file.endswith((".py", ".ipynb", ".yaml", ".json", ".md")):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        for idx, line in enumerate(f, 1):
                            for pattern in secret_patterns:
                                if pattern.search(line):
                                    # Skip false positives in configs/utils
                                    if "your_github_token_here" in line or "api_key" in file:
                                        continue
                                    if file_path not in secrets_found:
                                        secrets_found[file_path] = []
                                    secrets_found[file_path].append(f"Line {idx}: {line.strip()}")
                except Exception as e:
                    pass
    return secrets_found

def check_large_files(project_root: str, max_size_mb: float = 10.0) -> List[str]:
    """Returns a list of files that are larger than max_size_mb and not ignored."""
    large_files = []
    # Simple check on files under project_root
    for root, dirs, files in os.walk(project_root):
        if ".git" in root:
            continue
        for file in files:
            file_path = os.path.join(root, file)
            try:
                size_mb = os.path.getsize(file_path) / (1024 * 1024)
                if size_mb > max_size_mb:
                    large_files.append(f"{file_path} ({size_mb:.2f} MB)")
            except Exception:
                pass
    return large_files
