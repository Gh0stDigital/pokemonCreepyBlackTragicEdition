#!/bin/bash
# v44 checks (from overhaul/): bash run_v44.sh  -- v43 suite + t52_v44.py (POKeMON LEAGUE as BLACK: MOON STONE)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v44.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v43.sh
for md in block shatter agatha normal; do
  echo "=== t52_v44.py $md"; timeout 1800 $PY -u t52_v44.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|Error|assert"
done
