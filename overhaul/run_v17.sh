#!/bin/bash
# v17 checks (from overhaul/): bash run_v17.sh  (needs qa/pallet_with_ghost.state from run_v3.sh / t1..t5)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v17.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v15.sh  # (+ t31 below on this ROM)
for t in hostage noghost full mu labfail ballfail ballno alldead girl_normal gyms; do
  echo "=== t31_v16.py $t"; timeout 2400 $PY -u t31_v16.py $t 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|Error|assert"
done
