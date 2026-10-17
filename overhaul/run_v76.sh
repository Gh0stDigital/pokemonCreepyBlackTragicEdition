#!/bin/bash
# v76 checks (from overhaul/): bash run_v76.sh  -- v75 suite + t84_v76.py (no encounters on TOWER 7F); the stands' new places are checked by t61 altar (AMBER right, HELIX top, DOME left)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v76.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v75.sh
echo "=== t84_v76.py tower7f"; timeout 3600 $PY -u t84_v76.py tower7f 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
