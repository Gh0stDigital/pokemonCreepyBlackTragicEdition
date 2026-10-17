Creepy Black — Mu Overhaul v75: POKeMON TOWER 7F channelers after a menu
=========================================================================

ROM:     Creepy_Black_Mu_v75.gb
SHA-256: 67c62e8ec2b1e23f1dcea1aa36d7ed1c2a8a98c58838b7d49e86d96b2ce8f11b
Input:   Creepy_Black_Mu_v74.gb. build_v75.py asserts every byte it replaces; manifest_v75.json logs them.

PROBLEM  On the top floor (7F, quest stage 5, until the ritual is over) the ten channelers (v53) are hidden with picture 0 when they are more than two
steps away (the GB draws ten sprites). InitMapSprites runs again on every redraw (START menu, after text, battle) and
  - gives a VRAM slot only to pictures some sprite has at that moment (v36 skips picture 0): with every channeler hidden the channeler picture got no slot,
    every channeler slot read 0 and no channeler was ever drawn again until the map was reloaded;
  - does NOT copy the tiles again on such a redraw, so any slot number that differs from the one of the map load shows another picture's tiles
    (pigtail girls instead of the hooded channelers; AGATHA's and the girl's slots shifted too).
FIX      Before InitMapSprites' body runs (v67 im67 -> app75, bank 31:4B00) objects 4-15 of 7F get the pictures of the object list back (only while stage 5, ritual
not over and the long object list is loaded: D464 = 5, D467 < 6, D4E1 >= 10, map 94), so every load and every redraw hands out the same slots as the map load;
ch53 hides / shows the channelers again in the next frame as before.
NOT CHANGED  The long object list still makes steps there ~25 frames instead of ~17 (15 objects): the game engine updates every sprite.

Tests: t83_v75.py tower (v74 fails: after a menu no channeler is drawn / wrong slots; v75 passes), t61_v53.py lore / door / altar / ritualstash, t35_v25.py items icon climax sprites agatha house.
