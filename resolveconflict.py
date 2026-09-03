#!/usr/bin/env python3
"""
resolve_conflicts.py

Removes git merge conflict markers from a file, keeping either
"ours" (local/HEAD) or "theirs" (remote/incoming) for every conflict
block found. Does NOT try to be clever about mixing lines from both
sides -- it picks one full side per block, which is the only way to
guarantee the result is still valid, runnable code.

USAGE:
    python3 resolve_conflicts.py <filename> ours
    python3 resolve_conflicts.py <filename> theirs

    ours    = keep everything between <<<<<<< and =======  (your local version)
    theirs  = keep everything between ======= and >>>>>>>  (the remote version)

A backup of the original file is saved as <filename>.bak before any changes.
"""

import sys
import shutil

def resolve(filepath, keep):
    if keep not in ("ours", "theirs"):
        print("Second argument must be 'ours' or 'theirs'")
        sys.exit(1)

    backup_path = filepath + ".bak"
    shutil.copy(filepath, backup_path)
    print(f"Backup saved to {backup_path}")

    with open(filepath, "r") as f:
        lines = f.readlines()

    output = []
    state = "normal"   # normal | ours | theirs
    conflict_count = 0

    for line in lines:
        if line.startswith("<<<<<<<"):
            state = "ours"
            conflict_count += 1
            continue
        elif line.startswith("======="):
            state = "theirs"
            continue
        elif line.startswith(">>>>>>>"):
            state = "normal"
            continue

        if state == "normal":
            output.append(line)
        elif state == keep:
            output.append(line)
        # else: skip line (it's the side we're discarding)

    with open(filepath, "w") as f:
        f.writelines(output)

    print(f"Resolved {conflict_count} conflict block(s), keeping '{keep}' side.")
    print(f"Review the file before committing: {filepath}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    resolve(sys.argv[1], sys.argv[2])