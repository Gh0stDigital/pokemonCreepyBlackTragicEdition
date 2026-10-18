Creepy Black — Mu Overhaul v78: the evolution passes through GHOST; GHOST leaves for good
==========================================================================================

ROM:     Creepy_Black_Mu_v78.gb
SHA-256: a00dc5797b476adfd862385a36f3ab65dbfbeeee03737911e8102bc744ffe64c
Input:   Creepy_Black_Mu_v77.gb. build_v78.py asserts every byte it replaces; manifest_v78.json logs them.

1. The evolution scene of the climax is now RED -> GHOST -> BLACK: the game's own evolution animation (bank 1E:7E34) runs twice - RED flickers into GHOST, then GHOST flickers into the
   BLACK silhouette (picture sheet: qa/v78_evo_sheet.png, made by t86 evo). Code: evo78 (2D:4B60) replaces the far call at 2D:4548; the text ("GHOST has transcended and become BLACK.") is as before.
2. GHOST leaves the party for good when BLACK is born: v25's do_post kept it when it was the only member (cp 2 / jr c,.keep, now nops); BLACK, PRETA and AZHI join right after (v38 black_join).
   (t86 alone: party GHOST + ????? -> after the climax BLACK, PRETA, AZHI; v77 kept GHOST there.) GHOST in a PC box is not touched (it has to be in the party for the climax).

Tests: t86_v78.py evo / alone; t35 climax/agatha, t46 join, t61 ritualstash, t85 climax pass.
