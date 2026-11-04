#!/bin/bash
# v97 checks (from overhaul/): bash run_v97.sh  -- v96 suite (v97 only rewords MR. MU's first question; t73_v65 intro covers it)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v97.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v96.sh
