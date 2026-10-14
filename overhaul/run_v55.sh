#!/bin/bash
# v55 checks (from overhaul/): bash run_v55.sh  -- v54 suite + t63_v55.py (LORELEI as BLACK)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v55.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v54.sh
for md in black normal; do
  echo "=== t63_v55.py $md"; timeout 3600 $PY -u t63_v55.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
done
