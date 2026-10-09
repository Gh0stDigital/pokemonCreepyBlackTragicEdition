#!/bin/bash
# v18 checks (from overhaul/): bash run_v18.sh  (needs qa/pallet_with_ghost.state from run_v3.sh / t1..t5)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v18.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v17.sh
for t in unlock giovanni normal; do
  echo "=== t32_v18.py $t"; timeout 2400 $PY -u t32_v18.py $t 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|Error|assert"
done
