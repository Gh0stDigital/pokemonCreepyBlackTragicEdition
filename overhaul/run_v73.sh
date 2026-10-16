#!/bin/bash
# v73 checks (from overhaul/): bash run_v73.sh  -- v72 suite + t81_v73.py (PRETA unveil text, FUJI/AGATHA lines, SAFFRON shamaness tile, SNORLAX after CURSE)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v73.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v72.sh
for md in scope fuji hostage saffron snorlax; do
  echo "=== t81_v73.py $md"; timeout 3600 $PY -u t81_v73.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
done
