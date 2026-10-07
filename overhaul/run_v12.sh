#!/bin/bash
# v12 checks (from overhaul/): bash run_v12.sh  (needs qa/pallet_with_ghost.state from run_v3.sh / t1..t5)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v12.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v10.sh
for t in tower tower_pre tower_normal silph_rocket silph route22 champion champion_curse; do
  echo "=== t25_blue.py $t"; timeout 1500 $PY -u t25_blue.py $t 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|Error|assert|murder"
done
