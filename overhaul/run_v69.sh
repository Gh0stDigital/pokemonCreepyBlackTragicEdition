#!/bin/bash
# v69 checks (from overhaul/): bash run_v69.sh  -- v68 suite + t77_v69.py (ordinary trainers sulk after CURSE + spare; trainers are marked beaten again)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v69.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v68.sh
for md in sulk normal kill; do
  echo "=== t77_v69.py $md"; timeout 3600 $PY -u t77_v69.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
done
