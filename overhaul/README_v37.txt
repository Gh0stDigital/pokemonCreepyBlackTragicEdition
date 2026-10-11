Creepy Black Mu v37 (on v36): BLACK's battle back picture is no longer cut off.

SHA-256: c7593900fa2c1b0bfd26d930700ff3db403c59096eb2e31346cb73495c102fc5
The battle screen shows only the top-left 28x28 pixels of a 32x32 back picture (7x7 tiles; RED's own back picture is
exactly 28x28). v27 nudged BLACK's silhouette 2 px right / 4 px down and drew its halo around it, so 139 pixels (the right
side and the bottom) were outside that window and the figure looked cut off in battle.
v37 keeps the same look (black silhouette + v27's small GHOST-style halo) and scales it so both fit the visible 28x28:
24 px wide + 2 px of halo on each side, flush with the bottom (red_ghost_fusion.fuse_back_fit, picture at 2D:7A00).
Repointed like v27: BLACK's species header, YOU-as-BLACK's header and the LoadPlayerBackPic stub (F:7CED).

Tests: t35_v25.py backpic now also counts pixels outside the visible 28x28 (v27: 139, v37: 0) and fails on any
(v26/v27 pictures exempt); qa_ref/v37_battle_compare.png = v36 vs v37 in a real battle as BLACK, qa_ref/v37_back_fit.png.
run_v37.sh = run_v36.sh on v37. Static: check_hooks.py 91 hooks, 0 problems.
Regression (run_v37.sh): PASS=271 FAIL=0.
