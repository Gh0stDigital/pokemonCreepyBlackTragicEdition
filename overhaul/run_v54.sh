#!/bin/bash
# v54 checks (from overhaul/): bash run_v54.sh  -- v53 suite + t62_v54.py (MOM among the channelers after the ritual)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v54.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v53.sh
for md in mom; do
  echo "=== t62_v54.py $md"; timeout 3600 $PY -u t62_v54.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
done
