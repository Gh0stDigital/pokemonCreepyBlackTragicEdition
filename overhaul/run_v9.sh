#!/bin/bash
# v9 checks (from overhaul/): bash run_v9.sh  (needs qa/pallet_with_ghost.state from run_v3.sh / t1..t5)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v9.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v8.sh
for t in "t23_v9.py mirage" "t23_v9.py candy" "t23_v9.py center"; do
  set -- $t; f=$1; shift
  echo "=== $f $*"; timeout 1500 $PY -u $f "$@" 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|Error|assert"
done
