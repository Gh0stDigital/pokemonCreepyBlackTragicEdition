#!/bin/bash
# v46 checks (from overhaul/): bash run_v46.sh  -- v45 suite + t54_v46.py (seven changes)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v46.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v45.sh
for md in start ball lv100 gates agatha; do
  echo "=== t54_v46.py $md"; timeout 1800 $PY -u t54_v46.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|Error|assert"
done
