#!/bin/bash
# v81 checks (from overhaul/): bash run_v81.sh  -- v80 suite + t89_v81.py (GHOST WALK: back picture after turn 2, field move with inverted screen, no encounters)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v81.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v80.sh
for md in battle field encounters normal; do
  echo "=== t89_v81.py $md"; timeout 3600 $PY -u t89_v81.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
done
