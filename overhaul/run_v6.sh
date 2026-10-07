#!/bin/bash
# v6 checks (from overhaul/): bash run_v6.sh  (needs qa/pallet_with_ghost.state: run run_v3.sh, or t1..t5, first)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v6.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
for t in "t17_cerulean_mu.py hidden" "t17_cerulean_mu.py full" t17_cerulean_mu t18_macabre t18b_heal; do
  set -- $t; f=$1; shift; [[ $f == *.py ]] || f=$f.py
  echo "=== $f $*"; timeout 900 $PY -u $f "$@" 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|Error|assert|turn|PP"
done
