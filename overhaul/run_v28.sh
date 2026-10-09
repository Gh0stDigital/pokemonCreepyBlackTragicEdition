#!/bin/bash
# v28 checks (from overhaul/): bash run_v28.sh  (needs qa/pallet_with_ghost.state from run_v3.sh / t1..t5)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v28.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v25.sh  # v3-v25 suite on this ROM + t35 backpic below
echo "=== t35_v25.py backpic"; timeout 600 $PY -u t35_v25.py backpic 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|Error|assert"
for t in panic exempt sight normal; do
  echo "=== t36_v28.py $t"; timeout 2400 $PY -u t36_v28.py $t 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|Error|assert"
done
echo "=== t37_kills_save.py"; timeout 2400 $PY -u t37_kills_save.py 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|Error|assert"
