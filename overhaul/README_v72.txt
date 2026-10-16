Creepy Black — Mu Overhaul v72: the SNORLAX glitch (and what it was hiding)
============================================================================
Built from v71 by build_v72.py.

THE BUG (present since the hack's own set 12 was made, v1-v71)
  Outdoor maps load a set of 11 sprite pictures. Entries 1-9 must be 12-tile walkers (VRAM slots 2-10) and entries 10-11 the two four-tile pictures (slots 0B / 0C): an object finds its VRAM
  slot as (position of its picture in the set) + 1. The hack's set 12 (vanilla set 8 with the gravestone 49 added) was [12 0C 0A 06 07 0F 2F 21 43 3D 49]: SNORLAX (43) sat at position 9,
  which is walker slot 10, so it was drawn with whatever walker graphics were left there (a GUARD, later a CHANNELER = "a normal NPC"). The ball (3D) was at position 10 = slot 0B, which holds
  the first four-tile picture the loader loaded = SNORLAX's tiles: every item ball on the routes that use set 12 (ROUTE 12 south, 13, 14, 15, 17, 16 west) was drawn as Snorlax pieces.
  A test sweep over every outdoor map confirms it: v71 had 2 wrong objects (the ROUTE 15 ball, the ROUTE 16 SNORLAX), v72 has none (253 objects checked).
FIXES
  1. Set 12 = [12 0C 0A 06 07 0F 2F 21 05 3D 49]: walker 05 back at position 9 (valid order); balls and gravestones are right on ROUTES 13, 14, 15, 17 and 16 west.
  2. ROUTE 12 south of y 21 uses vanilla set 8 [... 05 3D 43] (SNORLAX at position 11 -> slot 0C, ball at 10 -> slot 0B). ROUTE 16 east already used set 5 (SNORLAX at 11).
  3. KNOWN LIMIT: set 8 has no gravestone picture (SNORLAX + BALL + GRAVESTONE are three four-tile pictures for two slots). A killed trainer on ROUTE 12 south used to be looked up
     past the end of the set and drawn with garbage tiles; the lookup (5:7A01) now stops after the set and HIDES an object whose picture is 49 and not in the set (every other missing
     picture behaves as before). So killed fishers on ROUTE 12 south vanish instead of leaving a gravestone (ROUTE 18 east, 19, 20, which also have no gravestone picture, now vanish too).
     A real gravestone there would need the ball as a walker-format picture (new art + object data); say if you want it.
CHECKS
  check_sets.py now also fails when any set has a four-tile picture in entries 1-9 / a walker in 10-11, and is region-aware (a split map's objects are checked against the set of their half).
  t80_v72.py: snorlax (after a battle reload: SNORLAX slot 0C with its tiles, balls slot 0B, a gravestone is hidden), sweep (every object of every outdoor map: slot and tiles), order.
NOT FIXED (existing since vanilla): a split map keeps its first set until the next full reload (a battle) - walking from ROUTE 12's north half into the south half, SNORLAX and the fishers are
drawn with the north set's tiles until a battle (or similar) reloads them.
