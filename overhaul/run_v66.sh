#!/bin/bash
# v66 checks (from overhaul/): bash run_v66.sh  -- v65 suite + t74_v66.py (sprite sets, PALLET shamaness)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v66.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v65.sh
for md in sets pallet; do
  echo "=== t74_v66.py $md"; timeout 3600 $PY -u t74_v66.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
done
