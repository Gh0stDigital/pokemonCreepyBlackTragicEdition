Creepy Black — Mu Overhaul v13: Pokémon Center / Mart freeze fixed, GHOST kept out of the heal, code audit
==========================================================================================================

ROM:     Creepy_Black_Mu_v13.gb
SHA-256: 2fa351de1eca04f63f96abe47469287eccfc3754f6437c0411d5f81ecf7098a4
Input:   Creepy_Black_Mu_v12.gb. build_v13.py asserts every byte it replaces; manifest_v13.json logs them.

1. FREEZE FIX (bug since v1)
   v1 replaced 15 bytes at 0x29FD (end of DisplayTextID) with a far call to the guard-bulletin check
   plus padding. 0x2A03 inside that range is AfterDisplayingTextID, a real entry point jumped to after
   the Pokémon Center nurse, Poké Mart clerks, vending machines and the cable club (jr at 0x29E5/0x29F8,
   jp at 0x2A7F/0x2ABA/0x2AC5). Since v1 that address held the 2nd byte of "call Bankswitch"
   ("18 36" = jr +$36), so after those dialogues the CPU jumped into the middle of CloseTextDisplay
   and the game froze. v13 restores the original first check at 0x29FD and starts the far call
   exactly at 0x2A03 (the bulletin routine already does the remaining checks).
   Verified: the same test freezes on v12 and runs through the nurse's/clerk's goodbye on v13.

2. GHOST AND THE POKéMON CENTER
   While the nurse heals, GHOST is taken out of the party: it is swapped to the last slot and the party
   count is lowered by one. So it isn't healed and gets no ball on the healing machine. Right after the
   machine animation it is put back in its original slot (species, data, OT and nickname all swapped
   back). Not done if GHOST is your only Pokémon. PRETA / AZHI are still skipped by the v9 rule.
   This is done in RAM rather than through the PC box, so a full box can never break it.
   Verified: party PRETA/GHOST/CHARMANDER at 5 HP -> party count 2 during the heal, CHARMANDER 22 HP,
   PRETA and GHOST still 5, GHOST back in slot 1, names unchanged.

3. AUDIT OF ALL CODE PATCHES (v1-v12)
   - Every patch that overwrote existing code was checked for jumps from the rest of the ROM landing
     inside it. Only 0x29FD was real (fixed above); the other hits were data bytes or the v3 encounter
     jumps that were retargeted on purpose.
   - Hooks that far-call into another bank were checked for registers the following code still
     needs. One real bug: v12's trainer-CURSE hook at F:5033 replaced "call CompareHLWithBC" (hl = the
     trainer's header pointer, bc = 0) with a far call that overwrote hl/b. So EVERY trainer looked
     "killable", including scripted ones (gym leaders, Giovanni, the Champion). The check now runs
     in home space (0x00ED) with the registers untouched, and only BLUE's RIVAL1/RIVAL2 classes are
     switched to the "GHOST hesitates" path. Champion BLUE is back to the base game's
     "But, it failed!" (RUN leaves).
   - All other hooks: the code after them only reads flags or memory, or the hook re-executes the
     replaced instructions.
