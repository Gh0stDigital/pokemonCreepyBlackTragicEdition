#!/bin/bash
# v98 checks (from overhaul/): bash run_v98.sh  -- v97 suite (v98 only rewords MR. MU's first question again; t73_v65 intro covers it)
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v98.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
CB_ROM=$CB_ROM PY=$PY bash run_v97.sh
