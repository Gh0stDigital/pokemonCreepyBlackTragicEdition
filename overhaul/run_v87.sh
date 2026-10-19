#!/bin/bash
# v87 checks (from overhaul/): bash run_v87.sh  -- v86 suite + t95_v87.py (BILL's cottage, the consort's sprite / house music, the CERULEAN cave guard)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v87.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v86.sh
for m in bill house cer normal; do
echo "=== t95_v87.py $m"; timeout 3600 $PY -u t95_v87.py $m 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
done
