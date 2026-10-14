#!/bin/bash
# v57 checks (from overhaul/): bash run_v57.sh  -- v55 suite + t65_v57.py (LANCE as BLACK)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v57.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v56.sh
for md in black normal; do
  echo "=== t65_v57.py $md"; timeout 3600 $PY -u t65_v57.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
done
