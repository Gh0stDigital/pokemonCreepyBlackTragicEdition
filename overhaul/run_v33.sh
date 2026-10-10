#!/bin/bash
# v33 checks (from overhaul/): bash run_v33.sh
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v33.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v32.sh  # everything up to v32 on this ROM 
echo "=== t42_v33.py"; timeout 600 $PY -u t42_v33.py 2>&1 | grep -E "PASS|FAIL|Error|assert"
