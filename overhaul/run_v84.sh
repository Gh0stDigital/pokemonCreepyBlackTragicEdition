#!/bin/bash
# v84 checks (from overhaul/): bash run_v84.sh  -- v83 suite + t91_v84.py (item balls vs black ball, SNORLAX, BLACK slides in) + t92_v84.py (DAMNATION faints, League name / MOON STONE order)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v84.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v83.sh
for md in balls free snorlax slide; do
  echo "=== t91_v84.py $md"; timeout 3600 $PY -u t91_v84.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
done
for md in damn damnwild names league bruno; do
  echo "=== t92_v84.py $md"; timeout 3600 $PY -u t92_v84.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
done
