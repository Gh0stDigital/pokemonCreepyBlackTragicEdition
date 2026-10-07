#!/bin/bash
# Full v2 regression chain. Usage: bash run_all.sh   (from overhaul/)
export PYTHONIOENCODING=utf-8; PY="${PY:-$TEMP/claude/cbvenv/Scripts/python}"
for t in t1_opening "t2_branch.py pokemon" "t2_branch.py trainer" t_sprites t3_story t4_rival t5_hunger t6_permadeath t7_curse t8b "t9_police.py forest_after_kill" "t9_police.py forest_after_kill 0" t10_wild; do
  set -- $t; f=$1; shift; [[ $f == *.py ]] || f=$f.py
  echo "=== $f $*"; timeout 600 $PY -u $f "$@" 2>&1 | grep -v -i sdl | grep -E "PASS|FAIL|RESULT|Error|assert|TEXT|curse_used|party|hunger|black" | grep -v "Bring out\|already out"
done
