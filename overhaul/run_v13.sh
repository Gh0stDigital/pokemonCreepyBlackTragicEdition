#!/bin/bash
# v13 checks (from overhaul/): bash run_v13.sh  (needs qa/pallet_with_ghost.state from run_v3.sh / t1..t5)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v13.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
PY=$PY bash run_checks.sh $CB_ROM || exit 1
CB_ROM=$CB_ROM PY=$PY bash run_v12.sh
for t in center mart; do
  echo "=== t26_center.py $t"; timeout 600 $PY -u t26_center.py $t 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|Error|assert|lowest"
done
echo "=== t27_saveload.py"; timeout 600 $PY -u t27_saveload.py 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|Error|assert"
