Creepy Black — Mu Overhaul v79: TOWER 7F after the ritual, MOM leaves the house
================================================================================

ROM:     Creepy_Black_Mu_v79.gb
SHA-256: 71445e6b2dba1c90662197a7ce5b6143879aeadd3766d76c0ca9a89816ac0717
Input:   Creepy_Black_Mu_v78.gb. build_v79.py asserts every byte it replaces; manifest_v79.json logs them.

1. Back on TOWER 7F as BLACK (RIT 6): AGATHA's sprite was drawn with wrong tiles and the channelers and the player's MOM (picture 33, object 15, v54) never showed up.
   Same cause as v75's channeler bug: the sprite loader (InitMapSprites, re-run on every redraw, e.g. each AGATHA text box) hands out VRAM slots from the pictures that are non-zero at that moment,
   but the tiles of the redraw are not copied again. v75's fix (app75: the object-list pictures of objects 4-15 before the loader) only ran while RIT < 6; after the ritual the long list
   is still loaded, ch54 hides the far channelers / MOM with picture 0, so they got no slot (image index FF = never drawn) and AGATHA's slot shifted.
   Now app75 runs whenever the long list is loaded (stage 5), and its table has MOM's picture (33) for object 15 (it said channeler: not the real list).
2. The player's house (map 25): from RIT 6 (BLACK) MOM is not there any more (new map script house79, bank 12:7200, hides object 1 every frame, then v25's script); the consort still waits there.

Tests (t87_v79.py): hall (AGATHA's slot stays, no black silhouette, the channelers near the player and MOM are drawn, MOM's confession; v78 fails the channelers / MOM checks), house (MOM before the ritual is over, gone at RIT 6).
t62 mom, t61 lore, t83 tower, t35 house (MOM now hidden) / agatha, t85 fossils pass. The old AGATHA look can be compared in qa/mom_cmp.png (v79: white-haired AGATHA; v78: a grey blob).
