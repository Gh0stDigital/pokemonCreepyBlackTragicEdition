#!/bin/bash
# v52 checks (from overhaul/): bash run_v52.sh  -- v51 suite + t60_v52.py (MR. MU locations, Mansion AMBER -> AZHI)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v52.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v51.sh
for md in cerulean mansion azhi; do
  echo "=== t60_v52.py $md"; timeout 2400 $PY -u t60_v52.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
done
