Creepy Black Mu v85 (on v84): the player's name stays BLACK after the POKeMON LEAGUE.
SHA-256: e3b0587001f22fa070482c328299c1c9ea73bfadb798cc007c364d5b9dd34e5b
v84 put RED back as soon as BLACK left the League rooms. Now the first time BLACK loads LORELEI's / BRUNO's / AGATHA's / LANCE's room (F5-F7, 71) the real name is backed up
in D879-D883 and the name (D158) becomes BLACK for good (D884 = 1); nothing restores it. BLUE's champion speeches say RED literally (v58) and are unchanged; texts that use the
player-name character (engine messages, other rival lines) now show BLACK from the League on. Not BLACK (GHOST route): unchanged.
Code: 2E:5D00 name85, map-load chain end 2E:42B4 -> name85 (name84 is unused now). Tests: t93_v85.py names (v84 fails the stay-BLACK checks); t92 names skips from v85. 
