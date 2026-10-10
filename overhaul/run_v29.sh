#!/bin/bash
# v29 checks (from overhaul/): bash run_v29.sh  (needs qa/pallet_with_ghost.state from run_v3.sh / t1..t5)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v29.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v28.sh  # everything up to v28 on this ROM, + the kill system below
for t in table nugget forest; do
  echo "=== t38_v29.py $t"; timeout 1200 $PY -u t38_v29.py $t 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|Error|assert"
done
