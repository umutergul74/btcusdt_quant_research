import json
import sys
from btc_quant.github.secret_scan import scan_path
print(json.dumps(scan_path(sys.argv[1] if len(sys.argv) > 1 else "."), indent=2))

