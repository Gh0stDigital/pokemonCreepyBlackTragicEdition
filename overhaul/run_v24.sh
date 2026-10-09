#!/bin/bash
# v24 checks (from overhaul/): bash run_v24.sh  (needs qa/pallet_with_ghost.state from run_v3.sh / t1..t5)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v24.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v23.sh  # + ????? sent out below
echo "=== t34_v23.py sendout"; timeout 2400 $PY -u t34_v23.py sendout 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|Error|assert"
