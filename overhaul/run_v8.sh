#!/bin/bash
# v8 checks (from overhaul/): bash run_v8.sh  (needs qa/pallet_with_ghost.state from run_v3.sh / t1..t5)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v8.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v7.sh
for t in t21_mansion_mu "t22_mirage_preta.py macabre" "t22_mirage_preta.py win"; do
  set -- $t; f=$1; shift; [[ $f == *.py ]] || f=$f.py
  echo "=== $f $*"; timeout 1500 $PY -u $f "$@" 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|Error|assert"
done
