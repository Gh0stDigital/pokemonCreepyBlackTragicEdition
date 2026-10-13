#!/bin/bash
# v53 checks (from overhaul/): bash run_v53.sh  -- v52 suite + t61_v53.py (channelers, the door after AGATHA's talk, the altar stash)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v53.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v52.sh
for md in lore door altar ritualstash; do
  echo "=== t61_v53.py $md"; timeout 3600 $PY -u t61_v53.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
done
