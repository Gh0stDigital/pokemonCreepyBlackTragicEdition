#!/bin/bash
# v7 checks (from overhaul/): bash run_v7.sh  (needs qa/pallet_with_ghost.state from run_v3.sh / t1..t5)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v7.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v6.sh
for t in t19_revive "t19_revive.py run" "t20_scope.py with" "t20_scope.py without"; do
  set -- $t; f=$1; shift; [[ $f == *.py ]] || f=$f.py
  echo "=== $f $*"; timeout 900 $PY -u $f "$@" 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|Error|assert|REVIVE|fainted on"
done
