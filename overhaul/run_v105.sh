#!/bin/bash
# v105 checks (from overhaul/): bash run_v105.sh  -- v104 suite + t106_v105.py (birds gone as BLACK, OAK without fought birds, fixed METAMORPHOSIS forms)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v105.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v104.sh
for md in birds oak fight "meta LORELEI" "meta BRUNO" "meta LANCE" "meta BLUE" "meta BILL"; do
  echo "=== t106_v105.py $md"; timeout 2400 $PY -u t106_v105.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
done
