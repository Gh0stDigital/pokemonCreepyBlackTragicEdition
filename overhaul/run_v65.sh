#!/bin/bash
# v65 checks (from overhaul/): bash run_v65.sh  -- v64 suite + t73_v65.py (MR. MU's first meeting in PALLET TOWN)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v65.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v64.sh
echo "=== t73_v65.py intro"; timeout 3600 $PY -u t73_v65.py intro 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
