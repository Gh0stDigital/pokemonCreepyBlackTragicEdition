#!/bin/bash
# v83 checks (from overhaul/): bash run_v83.sh  -- v82 suite + t90_v83.py (METAMORPHOSIS = CURSE for trainers, solid black pictures)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v83.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v82.sh
for md in trainer normal holes; do
  echo "=== t90_v83.py $md"; timeout 3600 $PY -u t90_v83.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
done
