#!/bin/bash
# v47 checks (from overhaul/): bash run_v47.sh  -- v46 suite (t49 CONSUME skipped) + t55_v47.py (METAMORPHOSIS, black POKeMON, CURSE)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v47.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v46.sh
for md in meta back status icon curse moves map bcurse normal; do
  echo "=== t55_v47.py $md"; timeout 1800 $PY -u t55_v47.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
done
