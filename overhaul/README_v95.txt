Creepy Black Mu v95 (on v94): METAMORPHOSIS on the map - the black ball stays put and the sprite goes when it is picked up
SHA-256: a40d294ca5c61ec55006fa219e4cb9033d26a66b15b0f0f7e7ae8291e1a3bb9a

BUG (since v74): a wandering NPC changed by METAMORPHOSIS kept walking around as the black ball, and after picking the ball up (the POKeMON joined) the ball sprite stayed on the map.
CAUSE: v74's killed74 (predef 0x13, per sprite per frame) called kill_chk2 (2D:6400) directly; v35-v73's killed13 called frame40 (2D:7E51), which holds the waiting-ball logic
(ball = movement STAY every frame, picked-up NPC hidden) around kill_chk2. The tests missed it because their freeze() sets every walker to STAY.
FIX: killed74 calls frame40 again (2D:6240 call 6400 -> call 7E51). Gravestones still stand still (the branch before it is untouched).
Tests (older ones, unfrozen walkers): t50_v42 still / reload, t48_v40 bane / persist (v94 fails 'the ball is gone', v95 passes), t82_v74 graves. run_v95.sh = run_v94.sh + these.
