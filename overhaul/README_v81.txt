Creepy Black Mu v81 (on v80): GHOST WALK fixes.
SHA-256: 8fba6e3b472e39afc76593a3f9cf389409cde07a9a511d058b0b0478598ba63d

1. Battle: GHOST WALK's second turn (CUT's animation, hit or miss) now gives BLACK's back picture back. Turn 1's TELEPORT slides the picture away
   and nothing restored it (it stayed missing for the rest of the battle). anim81 (bank 31) runs v48's animation hook and then 1E:53D7
   AnimationShowMonPic after GHOST WALK (the F:7F56 far-call target is anim81).
2. Field move: BLACK's party menu lists CURSE and GHOST WALK. Selecting GHOST WALK toggles "ghost walk" (event-flag byte D878, saved with the game,
   cleared by NEW GAME): text "BLACK slips into the dark. The POKeMON can't find you." / "BLACK steps back into the light.".
   While on: the whole screen is inverted (BGP 1B, OBP0 2F, OBP1 1F; menus, towns, buildings) and there are no wild encounters at all (MIRAGE
   included). Selecting it again turns both off at once. In battle the palette stays normal (the v48 negative animations rely on it); the filter comes
   back when the battle ends.

Technical:
- Palette: 0:20E7 LoadGBPal rewritten shorter (row = 2143 - wMapPalOffset in page 21) and ends with jp core81 (0:35BF): flag on and wIsInBattle 0 ->
  the row (hl on its third byte) is written complemented, OBP1 first. VBlank handler (0:20C6 audio far call) -> vbl81 (0:1251): OBP0 = D0 (the normal
  overworld palette, also what GBPalNormal / the last fade step leave) and flag on -> core81 with hl = 0:2145 (the normal row) - absolute writes, so a
  VBlank landing in the middle of LoadGBPal can't double-invert.
- Encounters: tow81 (4:7BD0) in front of v76's tow76 (hook at 4:78BC).
- Party menu: field-move tables moved to 1:7E60 (entry 11 = AB GHOST WALK, name 11, menu x 8; names after CURSE), dispatch fm81 (4:7BDC) reads the
  handler word of entry 11 (ca 2b = bytes of 4:71DC) and sends it to gwalk81 (bank 31:5715) like v41 did for entry 10.
- Test: t89_v81.py battle / field / encounters / normal; run_v81.sh = run_v80.sh + t89.
