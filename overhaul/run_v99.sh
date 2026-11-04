#!/bin/bash
# v99 checks (from overhaul/): bash run_v99.sh  -- v98 suite + t104_v99.py (CINNABAR GYM quiz trainers killable, quiz machine error, BLAINE's speeches)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v99.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v98.sh
for md in kill spare quiz blaine lore; do
  echo "=== t104_v99.py $md"; timeout 2400 $PY -u t104_v99.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
done
