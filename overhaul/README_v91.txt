Creepy Black Mu v91 (on v90): the cave tile bug (MT. MOON, ROCK TUNNEL, CERULEAN CAVE, VICTORY ROAD, DIGLETT'S CAVE ... = the CAVERN tileset)
SHA-256 32624ec9639b60dcba59d009b5a157ae3ecc60e28d2baf2007c95d949d192bf8

CAUSE: v20 / v21 drew the TOWER CHAMBER with 15 new blocks they stored as "Tower blockset slots 6E-7C" at 1B:4CA0-4D8F, believing the Tower blockset (1B:45C0) had 176 slots.
It has 110 ($6E): 1B:4CA0 is the first 240 bytes of the CAVERN TILESET'S GRAPHICS (tiles 0-14). Since v20 every cave map drew 15 wrong tiles (walls / floor).
FIX: the original 240 bytes are back at 1B:4CA0 (identical to v1 / v19). The TOWER tileset (graphics $5C0 bytes + 110 blocks + the 15 chamber blocks = 125 blocks, slots 00-7C) lives in bank 32:6000
(gfx 6000, blocks 65C0) and its header (0:C872: bank, blocks ptr, gfx ptr) points there; slots 7D+ of that block area are free for new blocks. The collision pointer is unchanged.
VERIFIED: VRAM tiles of MT. MOON / ROCK TUNNEL / CERULEAN CAVE / DIGLETT'S CAVE / the dummy cave maps = v19's, byte for byte; POKeMON TOWER and the CHAMBER give the same VRAM tiles and tile map as v90.
Tests: t99_v91.py (v90 fails the cave checks, v91 passes). run_v91.sh = run_v90.sh + t99.
