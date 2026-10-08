#!/bin/bash
# v15 checks (from overhaul/): bash run_v15.sh  (needs qa/pallet_with_ghost.state from run_v3.sh / t1..t5)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v15.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v14.sh
for t in cer_curse cer_win cer_normal cer_curse_nomurder cer_shock_skip bill; do
  echo "=== t30_v15.py $t"; timeout 1500 $PY -u t30_v15.py $t 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|Error|assert"
done
