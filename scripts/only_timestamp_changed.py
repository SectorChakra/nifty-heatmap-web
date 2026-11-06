"""Exit 0 if the staged data files differ from HEAD ONLY in `generatedAt`.

The fetch runs every minute, all day. Outside market hours prices do not move,
so the only difference is the timestamp -- and committing that anyway started
a GitHub Pages deploy every minute, 24x7 (~1,400 a day), which clogged the
account's Pages queue. A commit that changes nothing a reader can see is skipped.
"""
import json
import subprocess
import sys

FILES = ["data.json", "sector_data.json"]


def load(text):
    doc = json.loads(text)
    doc.pop("generatedAt", None)
    return doc


for f in FILES:
    try:
        old = subprocess.run(["git", "show", f"HEAD:{f}"], capture_output=True,
                             text=True, check=True).stdout
    except subprocess.CalledProcessError:
        sys.exit(1)                      # new file: a real change
    with open(f) as fh:
        if load(old) != load(fh.read()):
            sys.exit(1)                  # prices or anything else moved
sys.exit(0)
