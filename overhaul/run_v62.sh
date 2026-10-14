#!/bin/bash
# v62 checks (from overhaul/): bash run_v62.sh  -- v61 suite + t70_v62.py (CERULEAN CAVE: PROF. OAK)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v62.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v61.sh
for md in scene block normal; do
  echo "=== t70_v62.py $md"; timeout 3600 $PY -u t70_v62.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
done
