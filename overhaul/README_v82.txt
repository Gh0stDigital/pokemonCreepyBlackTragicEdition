Creepy Black Mu v82 (on v81): the text when a POKeMON is added by METAMORPHOSIS.
SHA-256: 074748e921748b3fefc78c9f1b45c9c686497890a169fb4fe20a61e36bab3946

"<MON> was ensnared!" replaces "<MON> joined your party." (party) and "<MON> was sent to the PC." (box: "<MON> was ensnared!" then
"It was sent to the PC."). Used by METAMORPHOSIS in battle (wild POKeMON, trainer's POKeMON, the trainer turned into a POKeMON) and by
picking up a black ball on the map (same routine, `give`). "The trainer became <MON>!" is unchanged.

Technical: the two old texts in 2F (420C party, 4224 box) are now TX_FAR (17 lo hi 31 50) to bank 31:5800 / its second text; tests t47_v39 / t48_v40
accept "ensnared" from v82 on. run_v82.sh = run_v81.sh (no new test file).
