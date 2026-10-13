#!/bin/bash
# v51 checks (from overhaul/): bash run_v51.sh  -- v50 suite + t59_v51.py (TOWER GHOST, LAVENDER music, MR. MU's quiet battle)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v51.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v50.sh
for md in lead switch only music mu; do
  echo "=== t59_v51.py $md"; timeout 2400 $PY -u t59_v51.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
done
