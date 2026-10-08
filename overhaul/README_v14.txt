Creepy Black — Mu Overhaul v14: Mirage rate fix, hungrier GHOST, YOU without a Poké Ball, GAMBLERs,
PRETA/AZHI off the Pokédex, killable gym leaders + revenge, killer rumours in towns
==========================================================================================================

ROM:     Creepy_Black_Mu_v14.gb
SHA-256: acd7ac590d4893b0edd0f0a01c5c1227fabd0c8166f1f8f3a14b5241322eeb46
Input:   Creepy_Black_Mu_v13.gb. build_v14.py (patchlib) asserts every byte it replaces; manifest_v14.json
         logs them. All 27 new hooks pass the patch guard (one reviewed data false positive, see below).

0. GHOST AWARD FIX (bug since v1, found by the v14 test chain)
   v1 moved the base game's GHOST award (AddPartyMon) from before the first rival battle to after it.
   AddPartyMon decides party vs. enemy party from wMonDataLocation (CC49), which the battle can leave
   non-zero (seen: 4). Then GHOST went into the ENEMY party: GHOST flag and hunger set, but no GHOST.
   Whether it happened depended on what went on in the rival battle. The award now clears CC49 first.
   Verified: the same saved state gives [CHARMANDER] on v13 and [CHARMANDER, GHOST] on v14.

1. MIRAGE RATE FIX
   The wild-encounter check only lets an encounter through when hRandomAdd < grass rate (Route 1: 25).
   The Mirage roll (2E:4326, v3) then compared the SAME hRandomAdd with its chance (2 per GHOST use,
   max 64). The grass rate is always below the chance once GHOST was used ~13 times, so EVERY encounter
   became the Mirage trainer. The roll now calls Random for a fresh number.
   Verified (Route 1, chance 64/256, 24 encounters): v13 = 0 wild / 11 Mirage; v14 = 19 wild / 5 Mirage.

2. GHOST HUNGER AT THE START
   Hunger starts at 67 instead of 160 when GHOST is awarded: 67 x 6 steps = ~400 steps to the first meal.

3. YOU (stand-in species 79) IN BATTLE
   When YOU is sent out there is no Poké Ball poof and no "growing out of the ball" animation: the picture
   is drawn at full size at once (SendOutMon F:4D0E / F:4D16). Other Pokémon are unchanged.
   Verified: Mirage battle with YOU leading -> 0 poof animations, back pic drawn; with a normal Pokémon
   leading -> 1 poof.

4. GENTLEMAN -> GAMBLER
   All 24 map NPCs that used the GENTLEMAN sprite now use the GAMBLER sprite (Pokémon Centers, S.S. Anne,
   houses, the SS Anne gentleman trainers...), and Saffron's outdoor sprite set swaps GENTLEMAN for
   GAMBLER. Mr. Mu is the only one left with the GENTLEMAN sprite (Pallet, Cerulean trade house,
   Pokémon Mansion 1F). The GENTLEMAN trainer class shows the GAMBLER battle picture (the class name
   stays GENTLEMAN). The Mirage trainer's blacked-out gentleman picture is a separate copy (unchanged).
   Verified: Viridian Pokémon Center sprite list has GAMBLER and no GENTLEMAN; trade house Mu = GENTLEMAN.

5. PRETA / AZHI ARE NOT KABUTOPS / AERODACTYL IN THE POKéDEX
   Meeting species B6 (PRETA) or B7 (AZHI) in battle no longer marks Kabutops/Aerodactyl as seen, and
   getting PRETA from Mr. Mu no longer marks Kabutops seen/owned (v6 did).
   Verified: Mirage battle vs AZHI -> dex bits for #141/#142 stay clear (v13 sets them); a wild Route 1
   Pokémon is still marked seen.

6. GYM LEADERS CAN BE KILLED WITH CURSE
   The base game already let CURSE kill BROCK (kill index 12 in its gravestone system: D4A4-D4AD is a bit
   field of killed trainers, D486 the per-map list of sprite -> kill index, D4AE/AF the index of the
   trainer being fought). v14 gives the other leaders their own indices: MISTY 26, LT.SURGE 27,
   ERIKA 28, KOGA 29, SABRINA 30, BLAINE 31, GIOVANNI 32 (Viridian Gym only; never used by the base).
   In the trainer phase after the win, CURSE on the leader now:
   - kills them like any trainer: murder flag (D453: police bulletins, town rumours), GHOST feeds;
   - after the battle "<PLAYER> took the <BADGE> from <LEADER>'s body." The badge and the leader's
     event are set and the TM is put in the bag silently (if there is room), so the story goes on;
   - the leader is a gravestone on every later visit (added to the D486 list at map load);
   - the gym trainers are NOT deactivated (a normal win still deactivates them). Any trainer you
     haven't beaten still fights, and their battle line becomes:
       "<LEADER> is dead! You murdered him/her!  I'll avenge my LEADER, murderer!"
   - BROCK keeps the base game's kill (badge, no TM, no text); only his gym trainer stays active now
     and swears revenge.
   RUN in the trainer phase spares the leader: normal badge/TM dialogue, trainers deactivated.
   Verified in the emulator: MISTY killed (murder, kill bit, badge + TM11, "took the CASCADEBADGE",
   the Jr. Trainer spots you with the revenge line and battles, MISTY is a gravestone on re-entry);
   MISTY spared (normal TM text, trainers deactivated, no murder); BROCK killed (trainer stays active,
   revenge line); KOGA killed (bank 1D code shared with BLAINE/GIOVANNI).
   The other gyms use the same generated code with their own addresses (all asserted by the build).

7. KILLER RUMOURS IN TOWNS
   After your first CURSE murder (D453), 14 flavour NPCs (no item, no needed information) talk about a
   trainer killing trainers and Pokémon, mixed up with TEAM ROCKET; before it they say their normal lines:
     Pallet girl, Viridian youngster, Pewter lass, Cerulean (2), Lavender, Vermilion (2),
     Celadon (2), Fuchsia, Cinnabar, Saffron (a ROCKET grunt before Silph, a citizen after).
   Each one is a small text script in the map's text bank that picks the rumour (bank 2E) or the
   original text.
   Verified: Pallet girl with/without a murder.

TOOLING
   - patchlib accepts hex strings for patch data; patchguard treats "xor a"/"sub a" as not reading a,
     and a stub path that pops its own return address as not returning to the hook site.
   - check_hooks.py now defaults to v14 (68 hooks, 0 problems). Reviewed: Saffron Gym victory hook,
     17:50FD is trainer-header data (30 b3 d7), not a jr.
   - t28_v14.py modes: mirage_rate, you, dex, gambler, rumour, misty_kill, misty_win, brock_kill, koga_kill.
     run_v14.sh = run_v13.sh + t28. harness.VERSION = ROM version (t4 expects hunger 67 from v14).

New saved RAM: kill bits D4A7 bits 2-7 and D4A8 bit 0 (inside the base game's gravestone bit field,
cleared on NEW GAME like the rest of D450-D4AD).
