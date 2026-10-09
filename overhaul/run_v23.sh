#!/bin/bash
# v23 checks (from overhaul/): bash run_v23.sh  (needs qa/pallet_with_ghost.state from run_v3.sh / t1..t5)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v23.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v22.sh  # + t34 below
for t in ritual no bagfull boxfull partyfull wild; do
  echo "=== t34_v23.py $t"; timeout 2400 $PY -u t34_v23.py $t 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|Error|assert"
done
