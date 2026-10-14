#!/bin/bash
# v61 checks (from overhaul/): bash run_v61.sh  -- v60 suite + t69_v61.py (BILL's team and picture)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v61.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v60.sh
echo "=== t69_v61.py"; timeout 3600 $PY -u t69_v61.py 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
