#!/bin/bash
# usage: pkg.sh PREV NEW  (e.g. 50 51): test ROM builds for NEW from PREV's, run_vNEW.sh skeleton must be written by hand
P=$1;N=$2
SHA=$(python3 -c "import hashlib;print(hashlib.sha256(open('Creepy_Black_Mu_v$N.gb','rb').read()).hexdigest())")
PSHA=$(python3 -c "import hashlib;print(hashlib.sha256(open('Creepy_Black_Mu_v$P.gb','rb').read()).hexdigest())")
for k in test chamber_test ritual_test mysave_test mysave2_test mysave3_test; do
  sed "s/V${P}_SHA/V${N}_SHA/g; s/$PSHA/$SHA/; s/v$P/v$N/g; s/V$P/V$N/g" build_v${P}_$k.py > build_v${N}_$k.py; python3 build_v${N}_$k.py | tail -1 | cut -c1-70
done
sed -i "s/(v1-v$P)/(v1-v$N)/; s/Creepy_Black_Mu_v$P.gb/Creepy_Black_Mu_v$N.gb/" check_hooks.py
sed -i "s/Creepy_Black_Mu_v$P.gb/Creepy_Black_Mu_v$N.gb/" run_checks.sh
PY=python3 bash run_checks.sh | tail -1
echo $SHA
