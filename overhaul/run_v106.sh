#!/bin/bash
# v106 checks (from overhaul/): bash run_v106.sh  -- v105 suite + t107_v106.py (ROCKET route part 1: PEWTER MUSEUM ROCKET, contract on BROCK)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v106.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v105.sh
for md in vis flow already witness; do
  echo "=== t107_v106.py $md"; timeout 2400 $PY -u t107_v106.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
done
