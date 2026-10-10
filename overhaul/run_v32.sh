#!/bin/bash
# v32 checks (from overhaul/): bash run_v32.sh  (needs qa/pallet_with_ghost.state from run_v3.sh / t1..t5)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v32.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v31.sh  # everything up to v31 on this ROM, + PRETA/AZHI immunity and PRETA's back
for t in immune back; do
  echo "=== t41_v32.py $t"; timeout 1500 $PY -u t41_v32.py $t 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|Error|assert"
done
