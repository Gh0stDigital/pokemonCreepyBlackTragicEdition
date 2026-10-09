#!/bin/bash
# v25 checks (from overhaul/): bash run_v25.sh  (needs qa/pallet_with_ghost.state from run_v3.sh / t1..t5)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v25.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
rm -f qa/*v25a*.state                      # t35's cached chamber states are per ROM build
CB_ROM=$CB_ROM PY=$PY bash run_v24.sh  # + t35 below
for t in items icon climax sprites you agatha house normal; do
  echo "=== t35_v25.py $t"; timeout 2400 $PY -u t35_v25.py $t 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|Error|assert"
done
