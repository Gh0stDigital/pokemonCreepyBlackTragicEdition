Creepy Black Mu v32 (on v31): GHOST can't eat PRETA or AZHI; PRETA's back picture has light-grey rib shading.

1. Hunger victim (v30 rules) skips PRETA (species B6) and AZHI (B7):
   - the nearest Pokemon in front of GHOST that it can eat, otherwise the nearest one below it (GHOST leading: just below);
   - nothing edible (only GHOST, PRETA, AZHI): GHOST eats the player (GENGAR's cry, save erased, title screen);
   - GHOST not in the party: the last edible one.
   The 50-step warning names the same victim. Code: victim2 (2D:6080); v30's victim (2D:5EED) jumps there.
2. PRETA (fossil KABUTOPS) back picture (B:7F3C): the 83 rib-line pixels v8 had turned white are light grey now
   (colour 1, the lightest shade); outline and the rest unchanged, no dark grey. preta_back.py, variant A of
   qa_ref/v32_preta_back_variants.png (B = v7's dark-grey ribs, C = + v6's light patches); before/after in
   qa_ref/v32_preta_back_compare.png.
Tests: t41_v32.py immune (PRETA in front -> eats below, AZHI in front -> eats further up, normal case, nothing edible ->
player) / back (only white -> light grey changed).
Regression (run_v32.sh: v3-v31 suites + t41): 228 PASS, 0 FAIL
