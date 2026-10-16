Creepy Black — Mu Overhaul v70: killed scripted grunts stay silent
==================================================================
Built from v69 by build_v70.py.

NUGGET BRIDGE Rocket (ROUTE 24) and the CERULEAN thief (behind the house): when you kill them with CURSE (v34 kill bits $1FD / $1FC = D44F bits 5 / 4) their
after-battle dialogue is no longer played. Everything the script sets before the text still fires:
  - Rocket: D7EF bit 1 (EVENT_BEAT_ROUTE24_ROCKET). The NUGGET was already given before the fight (his first speech), so nothing is lost.
  - Thief: D75B bit 7 (EVENT_BEAT_CERULEAN_ROCKET_THIEF), and the event's world change that his speech triggers after the TM28 (fade out / in, object 7 shown, 9 and 6 hidden:
    the house guard moves away) is run directly (1D:4872). TM28 (part of his speech) is NOT given when he is dead.
Alive: unchanged (both texts, TM28). The other two scripted grunts (MT. MOON B2F Super Nerd, GAME CORNER Rocket) are untouched.
Tests: t78_v70.py route24 / cerulean (the post-battle map script is started with the kill bit set / clear): flags, script finished, text shown only when alive, toggles.
