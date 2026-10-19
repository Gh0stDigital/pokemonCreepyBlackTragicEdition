#!/bin/bash
# v85 checks (from overhaul/): bash run_v85.sh  -- v84 suite + t93_v85.py names (the player's name stays BLACK after the LEAGUE)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v85.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v84.sh
echo "=== t93_v85.py names"; timeout 3600 $PY -u t93_v85.py names 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
