#!/bin/bash
# v36 checks (from overhaul/): bash run_v36.sh
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v36.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v35.sh  # everything up to v35 on this ROM
for md in tower agatha cap giovanni blue blue_normal; do
  echo "=== t45_v36.py $md"; timeout 1500 $PY -u t45_v36.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|Error|assert"
done
