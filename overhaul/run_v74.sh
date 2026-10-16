#!/bin/bash
# v74 checks (from overhaul/): bash run_v74.sh  -- v73 suite + t82_v74.py (CINNABAR/town signs, GAME CORNER Rocket, gravestones stay put, MANSION statue switch)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v74.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v73.sh
for md in signs towns gamecorner graves statue; do
  echo "=== t82_v74.py $md"; timeout 3600 $PY -u t82_v74.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
done
