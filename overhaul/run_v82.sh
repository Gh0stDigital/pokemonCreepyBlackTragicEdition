#!/bin/bash
# v82 checks (from overhaul/): bash run_v82.sh  -- v81 suite (t47/t48 expect "was ensnared!" from v82 on)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v82.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v81.sh
