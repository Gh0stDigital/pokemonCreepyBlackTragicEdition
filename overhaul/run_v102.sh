#!/bin/bash
# v102 checks (from overhaul/): bash run_v102.sh  -- v101 suite + t69_v61.py (BILL's team by name: FLAREON first)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v102.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v101.sh
echo "=== t69_v61.py"; timeout 3600 $PY -u t69_v61.py 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
