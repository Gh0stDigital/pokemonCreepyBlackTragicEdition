Creepy Black Mu v83 (on v82): METAMORPHOSIS towards trainers, solid black pictures.
SHA-256: b50935836caa17a1988f1a92e7024dd1019bd7fad475cf2553704758517bab45

1. METAMORPHOSIS on a trainer's POKeMON now behaves like CURSE as far as the trainer and the battle screen go:
   - no faint animation and no "Enemy <MON> fainted!" (the curse-kill flag CC39 = 1 is set; it is what CURSE does and what the faint code looks at),
   - D452 ("CURSE used this battle") is set, so everything that keys on it fires as for CURSE: the trainer's frightened end-of-battle line
     ("What have you done!?"), the v69 sulking afterwards, the v71 notoriety, BLUE's replacement POKeMON (v45).
   Wild METAMORPHOSIS is unchanged (the battle ends like an escape, no faint text, D452 untouched).
2. Pitch-black pictures (the back picture of a POKeMON gained by METAMORPHOSIS, its status-screen picture) are solid silhouettes: v47 only turned the
   non-white pixels black, so white bodies (e.g. SEEL-like POKeMON) and eyes/highlights stayed white inside the outline. v83 fills every white pixel that
   has black pixels to its left and right in its row AND above and below it in its column (gaps between legs/arms stay open).
Technical:
- 2F:4069 (bane_move, trainer branch) far-calls meta83 (bank 31:5900): enemy HP 0, CC39 = 1, D452 = 1.
- 2F:7676 / 2F:7693 (back47 / front47: call blacken + ld de,$a188) far-call fill83 (bank 31:5980): far-calls blacken, then pass 1 (first/last black row of
  each of the 56 pixel columns in sSpriteBuffer0 $A000/$A038), pass 2 (per row: xmax, then fill), ends with ld de,$A188 (d/e survive the far call).
  Pixel (x,y) = byte $A188 + 2*y + 112*(x>>3), bit 7-(x&7) (tile = column*7 + row).
- Tests: t90_v83.py trainer / normal / holes. run_v83.sh = run_v82.sh + t90.
