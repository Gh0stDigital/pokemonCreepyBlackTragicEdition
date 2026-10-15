#!/bin/bash
# v64 checks (from overhaul/): bash run_v64.sh  -- v63 suite + t72_v64.py (the secret door in the HALL OF FAME)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v64.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v63.sh
for md in black normal; do
  echo "=== t72_v64.py $md"; timeout 3600 $PY -u t72_v64.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
done
