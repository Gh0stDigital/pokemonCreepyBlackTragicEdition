#!/bin/bash
# v71 checks (from overhaul/): bash run_v71.sh  -- v70 suite + t79_v71.py (notoriety counter, bribed Saffron gate guards)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v71.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v70.sh
for md in gates notor; do
  echo "=== t79_v71.py $md"; timeout 3600 $PY -u t79_v71.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
done
