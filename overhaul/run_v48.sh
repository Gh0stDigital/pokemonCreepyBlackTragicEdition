#!/bin/bash
# v48 checks (from overhaul/): bash run_v48.sh  -- v47 suite + t56_v48.py (GHOST WALK, DAMNATION, negative animations, AZHI)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v48.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v47.sh
for md in moves gwalk damnwild damntr macabre normal azhi moon; do
  echo "=== t56_v48.py $md"; timeout 1800 $PY -u t56_v48.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
done
