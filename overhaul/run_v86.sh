#!/bin/bash
# v86 checks (from overhaul/): bash run_v86.sh  -- v85 suite + t94_v86.py (Route 22 gate, fanfare, GHOST WALK power, Hall of Fame, OAK LAB aide)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v86.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v85.sh
for m in gate gw fanfare hof lab; do
echo "=== t94_v86.py $m"; timeout 3600 $PY -u t94_v86.py $m 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
done
