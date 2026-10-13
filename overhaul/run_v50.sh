#!/bin/bash
# v50 checks (from overhaul/): bash run_v50.sh  -- v49 suite + t58_v50.py (PRETA / AZHI: nervous, anxious, revival, levels)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v50.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v49.sh
for md in nervous anxious revive posthp preta25 xitem ritual; do
  echo "=== t58_v50.py $md"; timeout 2400 $PY -u t58_v50.py $md 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|SKIP|Error|assert"
done
