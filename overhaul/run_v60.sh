#!/bin/bash
# v60 checks (from overhaul/): bash run_v60.sh  -- v59 suite + t68_v60.py (BILL's cottage)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v60.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v59.sh
for md in black normal; do
  echo "=== t68_v60.py $md"; timeout 3600 $PY -u t68_v60.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
done
