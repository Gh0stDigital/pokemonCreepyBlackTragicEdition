#!/bin/bash
# v59 checks (from overhaul/): bash run_v59.sh  -- v58 suite + t67_v59.py (OAK'S LAB after the League)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v59.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v58.sh
echo "=== t67_v59.py black"; timeout 3600 $PY -u t67_v59.py black 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
