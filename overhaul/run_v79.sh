#!/bin/bash
# v79 checks (from overhaul/): bash run_v79.sh  -- v78 suite + t87_v79.py (TOWER 7F after the ritual: AGATHA, channelers, MOM; MOM gone from the house)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v79.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v78.sh
for md in hall house; do
  echo "=== t87_v79.py $md"; timeout 3600 $PY -u t87_v79.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
done
