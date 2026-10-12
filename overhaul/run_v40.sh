#!/bin/bash
# v40 checks (from overhaul/): bash run_v40.sh  -- v39 suite (t36 panic hands over to t48) + t48_v40.py (BANE on the map)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v40.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v39.sh
for md in bane persist overflow trainer; do
  echo "=== t48_v40.py $md"; timeout 1500 $PY -u t48_v40.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|Error|assert"
done
