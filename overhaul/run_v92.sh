#!/bin/bash
# v92 checks (from overhaul/): bash run_v92.sh  -- v91 suite (t60 azhi skipped) + t100_v92.py (Mansion MR. MU: key, AMBER check, warnings, gone after leaving)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v92.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v91.sh
echo "=== t100_v92.py talk"; timeout 2400 $PY -u t100_v92.py talk 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
