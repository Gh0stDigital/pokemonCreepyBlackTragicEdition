#!/bin/bash
# v45 checks (from overhaul/): bash run_v45.sh  -- v44 suite + t53_v45.py (BLUE replaces CURSEd POKeMON)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v45.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v44.sh
for md in tower normal silph chain champion; do
  echo "=== t53_v45.py $md"; timeout 1800 $PY -u t53_v45.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|Error|assert"
done
