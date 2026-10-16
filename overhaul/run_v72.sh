#!/bin/bash
# v72 checks (from overhaul/): bash run_v72.sh  -- v71 suite + t80_v72.py (SNORLAX / balls / gravestones, every outdoor object's VRAM slot) + check_sets.py (set order)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v72.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v71.sh
for md in snorlax sweep order; do
  echo "=== t80_v72.py $md"; timeout 3600 $PY -u t80_v72.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
done
