#!/bin/bash
# v38 checks (from overhaul/): bash run_v38.sh  -- v37 suite (t35 climax expects BLACK + PRETA + AZHI) + t46_v38.py
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v38.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v37.sh
for md in join owned card faint exp items pc daycare poison; do
  echo "=== t46_v38.py $md"; timeout 1500 $PY -u t46_v38.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|Error|assert"
done
