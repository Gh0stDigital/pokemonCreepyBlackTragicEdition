#!/bin/bash
# v39 checks (from overhaul/): bash run_v39.sh  -- v38 suite + t47_v39.py (BANE in battle)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v39.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v38.sh
for md in wild wildbox immune trainer migrate; do
  echo "=== t47_v39.py $md"; timeout 1500 $PY -u t47_v39.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|Error|assert"
done
