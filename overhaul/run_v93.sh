#!/bin/bash
# v93 checks (from overhaul/): bash run_v93.sh  -- v92 suite + t101_v93.py (ritual HUD levels / silent death + catch, GHOST battle start, OAK gone, Route 22 gate)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v93.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v92.sh
for md in ritual control climax oak gate; do
  echo "=== t101_v93.py $md"; timeout 2400 $PY -u t101_v93.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
done
