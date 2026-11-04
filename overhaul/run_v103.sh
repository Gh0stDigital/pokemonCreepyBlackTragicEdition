#!/bin/bash
# v103 checks (from overhaul/): bash run_v103.sh  -- v102 suite (v103 only redraws BLACK's back picture with a white eye; t54 start / t35 backpic cover it)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v103.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v102.sh
