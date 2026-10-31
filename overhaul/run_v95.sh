#!/bin/bash
# v95 checks (from overhaul/): bash run_v95.sh  -- v94 suite + the METAMORPHOSIS-on-the-map tests that v74-v94 broke (t50 still/reload, t48 bane/persist, t82 graves)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v95.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v94.sh
for a in "t50_v42.py still" "t50_v42.py reload" "t48_v40.py bane" "t48_v40.py persist" "t82_v74.py graves"; do
  echo "=== $a"; timeout 2400 $PY -u $a 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
done
