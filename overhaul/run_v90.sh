#!/bin/bash
# v90 checks (from overhaul/): bash run_v90.sh  -- v89 suite + t98_v90.py (BROCK after the fight: killed / spared after CURSE / normal win)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v90.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v89.sh
for m in kill spare win; do
echo "=== t98_v90.py $m"; timeout 3600 $PY -u t98_v90.py $m 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
done
