#!/bin/bash
# v104 checks (from overhaul/): bash run_v104.sh  -- v103 suite (v104 only moves BLACK's back-picture eye down)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v104.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v103.sh
