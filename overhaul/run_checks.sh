#!/bin/bash
# Static safety checks (from overhaul/): bash run_checks.sh [ROM]   -- no emulator needed, run before every release.
#  1. test_patchguard.py: the guard still catches the two bugs we shipped (v1 0x29FD, v12 F:5033)
#  2. check_hooks.py:     every hook ever added passes the guard on the given ROM (default: latest)
PY="${PY:-python}"
$PY test_patchguard.py && $PY test_patchlib.py && $PY check_hooks.py ${1:-Creepy_Black_Mu_v29.gb} | tail -1
