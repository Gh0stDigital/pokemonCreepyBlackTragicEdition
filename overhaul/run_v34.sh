#!/bin/bash
# v34 checks (from overhaul/): bash run_v34.sh
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v34.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v33.sh  # everything up to v33 on this ROM, + instant gravestones below
for mp in 23 41 33; do
  echo "=== t43_v34.py instant $mp"; timeout 1200 $PY -u t43_v34.py instant $mp 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|Error|assert"
done
