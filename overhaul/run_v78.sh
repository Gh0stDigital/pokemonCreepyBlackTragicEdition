#!/bin/bash
# v78 checks (from overhaul/): bash run_v78.sh  -- v77 suite + t86_v78.py (evolution RED -> GHOST -> BLACK, GHOST gone even when it was the only member)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v78.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v77.sh
for md in evo alone; do
  echo "=== t86_v78.py $md"; timeout 3600 $PY -u t86_v78.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
done
