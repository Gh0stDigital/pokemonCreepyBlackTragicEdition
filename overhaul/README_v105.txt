Creepy Black Mu v105 (on v104): the legendary birds and the story trainers' METAMORPHOSIS forms
SHA-256: c2b9598be23c3122f6ea1cd53e4942756e6db3ee2fe8125d0d8a4b98b67d7f4c

1. As BLACK the three legendary birds are gone from their places (PROF. OAK has caught them): ZAPDOS (POWER PLANT), MOLTRES (VICTORY
   ROAD 2F), ARTICUNO (SEAFOAM ISLANDS B4F). bird105 (2E:7F80, new first link of the 2E:4000 map-load chain) sets their show/hide bits
   (toggles 85 / 91 / 227 = D5B0 bit 5, D5B1 bit 3, D5C2 bit 3) whenever a map loads with D46C set. Before the ritual they are where they were.
2. PROF. OAK's final party (class 26 decimal = $1A, party 2) leaves out every bird the player fought before (killed or caught): the
   bird's own trainer-header flag (ZAPDOS D7D4 bit 1, MOLTRES D7EE bit 6, ARTICUNO D882 bit 2; the base game sets it after the fight).
   oak105 (E:7F20) sits in front of v45's ReadTrainer stub (call at E:5CE6) and returns without AddPartyMon for such a bird.
3. METAMORPHOSIS in the trainer phase gives a fixed POKeMON for: LORELEI -> GOLDEEN, BRUNO -> GOLEM, LANCE -> CHARIZARD,
   BLUE (champion, class $2B) -> FEAROW, BILL (class 26 party 1) -> MR. MIME. meta105 (2F:5F00) replaces bane_phase's call rand_uncaught
   (2F:4159); every other trainer (PROF. OAK too) still becomes a random POKeMON not caught yet.

Tests: t106_v105.py birds (gone as BLACK, there otherwise) / oak (no bird fought, ZAPDOS fought, all three fought) / fight (beating
ZAPDOS sets its flag and hides it) / meta LORELEI BRUNO LANCE BLUE BILL; controls: t47_v39.py trainer (random form for an ordinary
trainer), t70_v62.py scene (OAK's battle).
Note: the first build compared BILL's class with $26 - class 26 is DECIMAL ($1A); the test caught it.
