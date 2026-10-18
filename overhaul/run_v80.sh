#!/bin/bash
# v80 checks (from overhaul/): bash run_v80.sh  -- v79 suite + t88_v80.py (BLACK: ordinary alive trainers speak scared before/after the battle; not BLACK: usual text)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v80.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v79.sh
for md in black normal; do
  echo "=== t88_v80.py $md"; timeout 3600 $PY -u t88_v80.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
done
