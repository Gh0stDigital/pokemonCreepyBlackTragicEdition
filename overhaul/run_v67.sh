#!/bin/bash
# v67 checks (from overhaul/): bash run_v67.sh  -- v66 suite + t75_v67.py (gym shock mode)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v67.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v66.sh
for md in shock sulk normal abandon leaders trainers abandon_all killall; do
  echo "=== t75_v67.py $md"; timeout 3600 $PY -u t75_v67.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
done
