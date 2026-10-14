#!/bin/bash
# v63 checks (from overhaul/): bash run_v63.sh  -- v62 suite + t71_v63.py (the ten SHAMANESSES in the towns)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v63.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v62.sh
for t in 0 1 2 3 4 5 6 7 8 0x0a; do
  echo "=== t71_v63.py town $t"; timeout 3600 $PY -u t71_v63.py town $t 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
done
for md in "town 1 black" "nogh 1"; do
  echo "=== t71_v63.py $md"; timeout 3600 $PY -u t71_v63.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
done
