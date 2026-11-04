#!/bin/bash
# v100 checks (from overhaul/): bash run_v100.sh  -- v99 suite + t105_v100.py (consort BADGE requirement: ERIKA 4, MISTY 6, SABRINA 8)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v100.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v99.sh
for md in MISTY ERIKA SABRINA; do
  echo "=== t105_v100.py $md"; timeout 2400 $PY -u t105_v100.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
done
