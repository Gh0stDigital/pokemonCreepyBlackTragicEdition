#!/bin/bash
# v75 checks (from overhaul/): bash run_v75.sh  -- v74 suite + t83_v75.py (TOWER 7F channelers after a menu redraw)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v75.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v74.sh
echo "=== t83_v75.py tower"; timeout 3600 $PY -u t83_v75.py tower 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
