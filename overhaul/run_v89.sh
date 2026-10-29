#!/bin/bash
# v89 checks (from overhaul/): bash run_v89.sh  -- v88 suite + t97_v89.py (ROUTE 22's first rival fight: shock flags, hesitation, shock speech)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v89.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v88.sh
for m in curse win; do
echo "=== t97_v89.py $m"; timeout 3600 $PY -u t97_v89.py $m 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
done
