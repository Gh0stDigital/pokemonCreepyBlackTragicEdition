#!/bin/bash
# v37 checks (from overhaul/): bash run_v37.sh  -- v36 suite on v37 (t35 backpic now also checks the visible 28x28)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v37.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v36.sh
