#!/bin/bash
# v31 checks (from overhaul/): bash run_v31.sh  (needs qa/pallet_with_ghost.state from run_v3.sh / t1..t5)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v31.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v30.sh  # everything up to v30 on this ROM, + GHOST back to slot 1 after a MIRAGE
for t in lead second; do
  echo "=== t40_v31.py $t"; timeout 1500 $PY -u t40_v31.py $t 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|Error|assert"
done
