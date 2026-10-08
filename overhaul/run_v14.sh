#!/bin/bash
# v14 checks (from overhaul/): bash run_v14.sh  (needs qa/pallet_with_ghost.state from run_v3.sh / t1..t5)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v14.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v13.sh
for t in mirage_rate you dex gambler rumour misty_kill misty_win brock_kill koga_kill; do
  echo "=== t28_v14.py $t"; timeout 1500 $PY -u t28_v14.py $t 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|Error|assert|RESULT"
done
