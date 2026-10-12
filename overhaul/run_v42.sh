#!/bin/bash
# v42 checks (from overhaul/): bash run_v42.sh  -- v41 suite + t50_v42.py (a BANEd NPC's black ball stays put)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v42.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v41.sh
for md in still reload; do
  echo "=== t50_v42.py $md"; timeout 1500 $PY -u t50_v42.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|Error|assert"
done
