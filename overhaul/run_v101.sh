#!/bin/bash
# v101 checks (from overhaul/): bash run_v101.sh  -- v100 suite + t71_v63.py as BLACK in all ten towns (no shamaness from v101)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v101.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v100.sh
for t in 0 1 2 3 4 5 6 7 8 0x0a; do
  echo "=== t71_v63.py town $t black"; timeout 2400 $PY -u t71_v63.py town $t black 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
done
