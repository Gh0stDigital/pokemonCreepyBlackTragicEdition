#!/bin/bash
# v10 checks (from overhaul/): bash run_v10.sh  (needs qa/pallet_with_ghost.state from run_v3.sh / t1..t5)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v10.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v9.sh
for t in bf fireblast dragonrage wild wild_bf player_bf sprites; do
  echo "=== t24_v10.py $t"; timeout 1500 $PY -u t24_v10.py $t 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|Error|assert"
done
