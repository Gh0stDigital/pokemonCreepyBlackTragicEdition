#!/bin/bash
# v49 checks (from overhaul/): bash run_v49.sh  -- v48 suite + t57_v49.py (scared POKeMON, status immunity, Tower, services)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v49.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v48.sh
for md in scared moon status bstatus tower services; do
  echo "=== t57_v49.py $md"; timeout 2400 $PY -u t57_v49.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
done
