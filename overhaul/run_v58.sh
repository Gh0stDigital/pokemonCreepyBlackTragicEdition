#!/bin/bash
# v58 checks (from overhaul/): bash run_v58.sh  -- v57 suite + t66_v58.py (BLUE as BLACK, the Hall of Fame / AGATHA scene)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v58.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v57.sh
for md in black normal; do
  echo "=== t66_v58.py $md"; timeout 3600 $PY -u t66_v58.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
done
