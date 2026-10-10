#!/bin/bash
# v35 checks (from overhaul/): bash run_v35.sh
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v35.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v33.sh  # everything up to v33 on this ROM (v34's instant-gravestone test t43 no longer applies)
for mp in 23 41 33; do
  echo "=== t44_v35.py vanish $mp"; timeout 1200 $PY -u t44_v35.py vanish $mp 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|Error|assert"
done
