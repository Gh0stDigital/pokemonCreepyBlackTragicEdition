#!/bin/bash
# v30 checks (from overhaul/): bash run_v30.sh  (needs qa/pallet_with_ghost.state from run_v3.sh / t1..t5)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v30.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v29.sh  # everything up to v29 on this ROM, + hunger warnings below
for t in warn eat player; do
  echo "=== t39_v30.py $t"; timeout 1200 $PY -u t39_v30.py $t 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|Error|assert"
done
