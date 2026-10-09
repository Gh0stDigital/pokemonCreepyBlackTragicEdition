Creepy Black Mu v27 (on v26)
BLACK's battle back picture is back at FULL size (v26 had shrunk it to 80%), but without the boxy look:
the silhouette keeps all its shape and is moved 2 px right / 4 px down in the 32x32 picture, and its GHOST-style halo is
small (reach 2: grey checker + light checker, no scattered outer dots). The top and sides keep room for the halo, so no
square edge shows. Picture at 2D:6F00 (116-ish bytes, see manifest_v27.json); same three pointers as v26 repointed
(BLACK header, YOU-as-BLACK header, F:7CED stub). Preview: qa_ref/v27_back_compare.png (v25 | v26 | v27), v27_back_variants*.png.
Tests: t35_v25.py backpic/sprites/you/climax PASS, run_checks.sh 85 hooks 0 problems. Full v3 regression not re-run (picture data + pointers only).
Build: python build_v27.py  (SHA in manifest_v27.json)
