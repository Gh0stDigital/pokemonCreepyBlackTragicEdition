Creepy Black Mu v64 (from v63): a secret door in the HALL OF FAME
SHA-256 d27e47f719ab121cd3656e694a16ba044227cce0038d6e0f952f384fab66194a

- The HALL OF FAME (map 76, bank 16) gets a third warp: the floor tile in the top-left corner (y1, x0) leads back to the POKeMON LEAGUE lobby (map AE, its
  warp 2 = the top door, as when coming back from LORELEI's room). Like the room's bottom door (back to the Champion's room) it fires when you walk INTO the
  room's left edge while standing on the tile (walk to the corner, then press left once more). Nothing marks it: it is secret.
- Mechanics: the map's object data (border, warps, signs, objects) is followed by the warp-to list (view pointer, y, x per warp: arrival positions); both were
  moved to 16:65D6 with the new entries (warp (1,0) -> AE/2, warp-to C6F4,1,0) and the header's object pointer (hdr +10) follows. A first attempt that moved
  only the object data left the warp-to list behind and arrival at the room became (0,0) - the same reason v58's object-list swap failed.
- Works as BLACK (the end of the League, after AGATHA's scene) and on the GHOST route (the room's two original doors keep working).
- Tests: t72_v64.py black (corner -> lobby, arrival at its top door, walking on, the lobby's top door still leads to LORELEI's room), normal (3 warps, the two
  originals unchanged). run_v64.sh = run_v63.sh + t72. Only this test was run for v64 (v54-v63 full regressions still outstanding).
