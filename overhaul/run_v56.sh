#!/bin/bash
# v56 checks (from overhaul/): bash run_v56.sh  -- v55 suite + t64_v56.py (BRUNO as BLACK)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v56.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v55.sh
for md in black normal; do
  echo "=== t64_v56.py $md"; timeout 3600 $PY -u t64_v56.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
done
