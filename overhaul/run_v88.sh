#!/bin/bash
# v88 checks (from overhaul/): bash run_v88.sh  -- v87 suite + t96_v88.py (PROF. OAK's scene: picture tiles stay, one "shatters", no sprite over the credits)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v88.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v87.sh
for m in oak lorelei; do
echo "=== t96_v88.py $m"; timeout 3600 $PY -u t96_v88.py $m 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
done
