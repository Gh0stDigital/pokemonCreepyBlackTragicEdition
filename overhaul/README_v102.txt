Creepy Black Mu v102 (on v101): BILL's first POKeMON is FLAREON
SHA-256: 2ef6562d4b02adcbc5bfd1543a9d244e741b94a6d2354ee011c99003e9c0882c

v61 meant BILL's team to be FLAREON 56, VAPOREON 56, JOLTEON 56, CHANSEY 56, ALAKAZAM 58, PORYGON 60, but wrote species $6A in slot 1,
which is MACHOP in this ROM (FLAREON = $67). v102 changes that one byte (party at E:7EF0, offset +2). t69 had checked the same wrong
number; it now checks the six species by the game's own name list (7:421E) and passes on v102 ("BILL sent out FLAREON!" on screen).
