Creepy Black — Mu Overhaul v73: five small fixes
=================================================

ROM:     Creepy_Black_Mu_v73.gb
SHA-256: 789db83fc9afcfe85773d64029e3441291ed206edf028661189cfd7ae72a580c
Input:   Creepy_Black_Mu_v72.gb. build_v73.py asserts every byte it replaces; manifest_v73.json logs them.

1. PRETA in the party (SILPH SCOPE effect): the Tower ghost text now reads "PRETA's sight unveiled the GHOST's identity!"
   The real SILPH SCOPE item keeps the original text. (stub 16:6800 pretatxt, text in bank 32 at 5000)
2. AGATHA on Tower 7F before the rescue: no more "tied up": "AGATHA: Hmph! These ROCKET brats got me and old FUJI! Get rid of them, child!"
3. MR. FUJI at home after the rescue (GHOST route only, not BLACK, AGATHA not gone): after the FLUTE line he says AGATHA is still in the TOWER and may have something to give you as thanks. (stub 7:772B fujitxt)
4. SAFFRON shamaness moved from beside SILPH CO. to (y24,x32); still replaces the town's last sprite slot.
5. SNORLAX: if CURSE was used in the battle (D452), the "return to the mountain" text is skipped; the flags still fire. (stub 16:6800 snorlax)

VERIFIED: t81_v73.py modes scope, fuji, hostage, saffron, snorlax; run_checks.sh: 163 hooks, 0 problems.
