#!/bin/bash
# v77 checks (from overhaul/): bash run_v77.sh  -- v76 suite + t85_v77.py (the ritual: chamber music, MR. MU's quiet start, no victory fanfare, fossils until BLACK, the climax turn order)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v77.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v76.sh
for md in chamber fossils climax victory; do
  echo "=== t85_v77.py $md"; timeout 3600 $PY -u t85_v77.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
done
