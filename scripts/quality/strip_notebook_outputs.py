import json
import sys
from pathlib import Path
for nb_path in Path(sys.argv[1] if len(sys.argv) > 1 else "notebooks").rglob("*.ipynb"):
    nb = json.loads(nb_path.read_text(encoding="utf-8"))
    for cell in nb.get("cells", []):
        cell["outputs"] = []
        cell["execution_count"] = None
    nb_path.write_text(json.dumps(nb, indent=2) + "\n", encoding="utf-8")
    print(nb_path)

