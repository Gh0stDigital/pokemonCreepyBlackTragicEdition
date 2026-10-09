#!/bin/bash
# v19 checks (from overhaul/): bash run_v19.sh  (needs qa/pallet_with_ghost.state from run_v3.sh / t1..t5)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v19.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v18.sh
for t in closed chamber saveload; do
  echo "=== t33_v19.py $t"; timeout 1500 $PY -u t33_v19.py $t 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|Error|assert"
done
