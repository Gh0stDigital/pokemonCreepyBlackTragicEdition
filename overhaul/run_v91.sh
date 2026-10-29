#!/bin/bash
# v91 checks (from overhaul/): bash run_v91.sh  -- v90 suite + t99_v91.py (cave graphics restored, Tower / chamber unchanged)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v91.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v90.sh
echo "=== t99_v91.py"; timeout 3600 $PY -u t99_v91.py 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
