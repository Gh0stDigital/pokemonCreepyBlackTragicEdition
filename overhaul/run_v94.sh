#!/bin/bash
# v94 checks (from overhaul/): bash run_v94.sh  -- v93 suite + t102_v94.py (evolution RED -> BLACK, no GHOST picture)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v94.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v93.sh
echo "=== t102_v94.py evo"; timeout 2400 $PY -u t102_v94.py evo 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
