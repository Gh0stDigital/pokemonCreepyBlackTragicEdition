#!/bin/bash
# v3 regression chain (from overhaul/): bash run_v3.sh
export PYTHONIOENCODING=utf-8 CB_ROM=${CB_ROM:-Creepy_Black_Mu_v3.gb}; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
for t in t1_opening "t2_branch.py pokemon" "t2_branch.py trainer" t_sprites t3_story t4_rival t5_hunger t6_permadeath t7_curse t8b t10_wild "t9_police.py forest_after_kill" "t9_police.py forest_after_kill 0" t11_mirage_find "t11_mirage_find.py only_ghost" "t13_mirage_outcomes.py fight" "t13_mirage_outcomes.py run" t14_only_ghost t15_aero; do
  set -- $t; f=$1; shift; [[ $f == *.py ]] || f=$f.py
  echo "=== $f $*"; timeout 900 $PY -u $f "$@" 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|RESULT|Error|assert|MIRAGE|party|escape|delay|black|curse_used|TEXT: .*(scared|MACABRE|BLACK|Go!)" | grep -v "Bring out\|already out"
done
