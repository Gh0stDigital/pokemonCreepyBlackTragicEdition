#!/bin/bash
# v70 checks (from overhaul/): bash run_v70.sh  -- v69 suite + t78_v70.py (killed NUGGET BRIDGE Rocket / CERULEAN thief don't talk, flags still fire)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v70.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v69.sh
for md in route24 cerulean; do
  echo "=== t78_v70.py $md"; timeout 3600 $PY -u t78_v70.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
done
