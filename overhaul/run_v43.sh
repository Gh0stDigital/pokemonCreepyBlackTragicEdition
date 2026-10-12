#!/bin/bash
# v43 checks (from overhaul/): bash run_v43.sh  -- v42 suite + t51_v43.py (black ball graphics on the map)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v43.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v42.sh
for md in look indoor; do
  echo "=== t51_v43.py $md"; timeout 1500 $PY -u t51_v43.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|Error|assert"
done
