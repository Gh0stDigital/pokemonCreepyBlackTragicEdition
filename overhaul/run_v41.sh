#!/bin/bash
# v41 checks (from overhaul/): bash run_v41.sh  -- v40 suite + t49_v41.py (CONSUME)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v41.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v40.sh
for md in consume full refuse normal; do
  echo "=== t49_v41.py $md"; timeout 1500 $PY -u t49_v41.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|Error|assert"
done
