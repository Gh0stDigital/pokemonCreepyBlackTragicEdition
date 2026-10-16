#!/bin/bash
# v68 checks (from overhaul/): bash run_v68.sh  -- v67 suite + t76_v68.py (MIRAGE chance by victims, none as BLACK)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v68.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v67.sh
echo "=== t76_v68.py"; timeout 3600 $PY -u t76_v68.py 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
