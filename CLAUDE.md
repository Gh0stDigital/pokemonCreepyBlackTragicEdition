# Pokémon Creepy Black — Tragic Edition (Mu overhaul)

Binary ROM hack of the 1 MiB Game Boy ROM "Pokémon Black (Creepy)". Every version is built by a
Python script that applies **logged patches with old-byte asserts** on top of the previous verified ROM.
Never overwrite an earlier ROM; build a new version (v6, v7, …) and keep ROM length exactly 1,048,576 bytes.

## Layout
- `Creepy_Black_Mu_v1.gb` … `v35.gb` (root and `overhaul/`): builds. Latest = **v35**
  (SHA-256 dc9dd28c7d8a5e3420b3ac3d40a4e42d855d883f18d0b2813de7412982ae65f9).
- Test ROMs `Creepy_Black_Mu_vN_test.gb` (`build_vN_test.py`): vN + a built-in save (GHOST route, CHARMANDER, just after
  the POKéDEX; made by `make_save_v14.py`, packed into 2E:6000) installed when the cartridge has no save (`t29_testrom.py`).
  Keep 2E:6000–67FF free in the main builds for it. `Creepy_Black_Mu_v19…v35_chamber_test.gb` = vN + a test-only save on Tower 7F
  at AGATHA stage 5 (`make_save_v19_chamber.py`, flags set directly). `Creepy_Black_Mu_v25_ritual_test.gb` / `v26…v35_ritual_test.gb` = a save in the
  TOWER CHAMBER right after MR. MU's ritual (????? in the party): `make_save_v25_ritual.py` plays the ritual in the emulator
  and saves through the START menu; walking out of the circle starts the v25 climax.
- `edit/`: original v1 handoff (v1 build.py, which needs the clean base ROM that is NOT in this repo).
- `overhaul/build_v2.py … build_v35.py`: each takes the previous version, checks its SHA, writes the next
  ROM + `manifest_vN.json` (before/after bytes per patch). READMEs: `README_v2.txt`, `README_v3.txt`, `README_v6.txt`, `README_v7.txt`, `README_v8.txt`, `README_v9.txt`, `README_v10.txt`, `README_v11.txt`, `README_v12.txt`, `README_v13.txt`, `README_v14.txt`, `README_v15.txt`, `README_v16.txt`, `README_v17.txt`, `README_v18.txt`, `README_v19.txt`, `README_v20.txt`, `README_v21.txt`, `README_v22.txt`, `README_v23.txt`, `README_v24.txt`, `README_v25.txt`, `README_v26.txt`, `README_v27.txt`, `README_v28.txt`, `README_v29.txt`, `README_v30.txt`, `README_v31.txt`, `README_v32.txt`, `README_v33.txt`, `README_v34.txt`, `README_v35.txt`.
- `overhaul/harness.py` + `t*.py`: PyBoy emulator tests. `run_all.sh` (v2 features), `run_v3.sh` (full chain
  including the Mirage tests), `run_v6.sh` (Cerulean Mu / PRETA / MACABRE; needs the chain's
  `pallet_with_ghost` state), `run_v7.sh` (v6 checks + PRETA revival / Silph Scope effect), `run_v8.sh`
  (v7 checks + Mansion Mu / PRETA in Mirage battles), `run_v9.sh` (v8 checks + PRETA vs PRETA,
  Rare Candy, Pokémon Center), `run_v10.sh` (v9 checks + AZHI / BLACK FLAME / ?????), `run_v11.sh` (same suite on v11), `run_v12.sh` (v10 suite + rival BLUE, t25_blue.py), `run_v13.sh` (v12 suite + Pokémon Center/Mart, t26_center.py), `run_v14.sh` (v13 suite + t28_v14.py: Mirage rate, YOU, dex, GAMBLER, rumours, gym leaders; `bfs_to` walks around obstacles), `run_v15.sh` (v14 suite + t30_v15.py: Nugget Bridge BLUE, BILL), `run_v16.sh` (v15 suite + t31_v16.py: AGATHA quest), `run_v17.sh` (same on v17), `run_v18.sh` (v17 suite + t32_v18.py: SILPH CO.), `run_v19.sh` (v18 suite + t33_v19.py: secret chamber), `run_v20.sh` / `run_v21.sh` (same on v20 / v21), `run_v22.sh` (+ chamber fossils), `run_v23.sh` (+ t34_v23.py: MR. MU's talk + ritual battle), `run_v24.sh` (+ t34 sendout: ????? back pic), `run_v25.sh` (+ t35_v25.py: items/icon/climax/sprites/you/agatha/house/normal; its chamber states are cached in `qa/*v25a*`, delete them when the chamber/7F code layout changes), `run_v28.sh` (+ t36_v28.py: NPC panic/curse, exempt NPCs, trainer sight; t37_kills_save.py), `run_v29.sh` (+ t38_v29.py: kill system), `run_v30.sh` (+ t39_v30.py: hunger warnings/victim/GENGAR), `run_v31.sh` (+ t40_v31.py: GHOST back to slot 1 after a MIRAGE), `run_v32.sh` (+ t41_v32.py: PRETA/AZHI never eaten, PRETA back shading), `run_v33.sh` (+ t42_v33.py: PRETA back shaded like its front), `run_v34.sh` (+ t43_v34.py: gravestone right after the battle; v34 only), `run_v35.sh` (v33 suite + t44_v35.py: killed trainers vanish at once). `Creepy_Black_Mu_vN_mysave_test.gb` = vN + the user's own save (`Creepy_Black_Mu_user.sav`). Tests chain through save states in `overhaul/qa/` (gitignored; the chain
  regenerates them starting at `t1_opening.py`). Select the ROM with `CB_ROM=Creepy_Black_Mu_v5.gb`.
- Assembler: `overhaul/sm83asm.py` (SM83 assembler built from `ref/instruction_set.py`: labels, `.local` labels, db/dw/ds,
  `farcall addr,bank` macro; `test_sm83asm.py` round-trips real ROM code byte for byte). v25's code is written in it.
- Patch safety (static, no emulator): `overhaul/patchguard.py` (SM83 decoder + checks), `overhaul/patchlib.py`
  (shared build helpers: `Rom.put/data/code/hook/finish`), `overhaul/check_hooks.py` (re-checks all hooks v1-v35, found through the manifests
  on a ROM; reviewed exceptions listed with reasons), `test_patchguard.py` / `test_patchlib.py` (the guard must
  still catch the v1 0x29FD and v12 F:5033 bugs). Run all with `bash run_checks.sh [ROM]`.
- `ref/`: reverse-engineering helpers. `red.gb` = vanilla Pokémon Red (US) for signature matching;
  `pokered.sym` = pret pokered symbols; `sig.py` locates vanilla routines in this ROM by masked byte
  signatures; `dis.py` = tiny disassembler (`python ref/dis.py ROM BANK ADDR N`); `pic.py` = Gen-1 pic
  (de)compressor.
- `pokeblack/charmap.asm`: pret pokered charmap (used by build text encoding and tests).

## Setup
`pip install pyboy pillow pypng`, then run from `overhaul/` with `PY=python bash run_v3.sh`
(scripts default to a Windows venv path; set `PY`). Set `PYTHONIOENCODING=utf-8`.

## Making a new version (v36+)
- Write `build_vN.py` with `from patchlib import *` (and `from sm83asm import asm` for non-trivial code): `Rom(input, expect_sha)`, put stubs with `rom.put`, then
  connect them with `rom.hook(site, call_bytes, name, old, provides=...)`. `provides` = registers/flags the hook
  sets on purpose (e.g. `('f',)` for a yes/no result). Edit other code with `rom.code`, tables/text/pics with `rom.data`.
  The build stops with REFUSED if a hook covers a jump target or breaks registers the game still needs; only pass
  `reviewed='reason'` after checking the disassembly yourself.
- Prefer hooking exactly one `call X` (3 bytes). If a far call is needed before code that reads hl/b, put the
  stub in home space or save/restore the registers.
- Add `check_hooks.py` entries for new hooks, run `bash run_checks.sh`, then the emulator suite.
- Every special-case change gets a test that the normal case still behaves as before (e.g. "a gym leader still
  can't be cursed to death" next to "BLUE hesitates").

## Rules learned the hard way
- Verify bank, CPU address and file offset before patching; pokered addresses are shifted in this ROM.
- Text lines ≤ 17 rendered chars (`#` renders as "POKé", 4 chars): the ▼ arrow eats column 18.
- Outdoor maps can only show sprites in their sprite set (Pallet = set 1 at 0x17AB9).
- Don't claim behavior works until a PyBoy test shows it.
- Never patch over an address other code jumps to: v1's 0x29FD hook covered AfterDisplayingTextID (0x2A03) and
  froze the game after every Center/Mart dialogue until v13. Check jump targets into a patched range first.
- A hook that far-calls (ld hl/ld b/call Bankswitch) destroys hl/b: never put one where the next code needs
  those registers (v12 F:5033 bug).
- Before AddPartyMon, set wMonDataLocation (CC49) = 0: after a battle it can still say "enemy" (v1 GHOST award lost
  GHOST that way until v14).
- The base game's gravestone system: D4A4–D4AD = bit field of killed trainers (kill index), D486 = per-map list
  (sprite, 0, index) built at map load from the table at 3:5096 (+ v14 leader list in 2E), D4AE/AF = index of the
  trainer being fought (0 = can't be killed), read from **trainer-header offset 0xA**. Killed trainers get sprite 0x49
  (gravestone). Indices 0–25 base, 26–32 v14 leaders, 33 MR. MU, 34–79 and $100–$1FB = v29 (every other trainer;
  $100+ bits live at D430–D44F, see 3:4DB9; $1FC–$1FF = v34 scripted grunts, D430–D44F now full). Map-load gravestones:
  table 2D:7180 (v34) via kill_chk2 (2D:6400). **Per frame**, the overworld sprite code (1:50AA) hides killed trainers through
  predef 0x13 (was 3:4DFB = base list only; since v35 killed13 at 2D:6200 = base list + kill_chk2): anything that adds kills must be
  visible to kill_chk2, or the dead trainer keeps standing until the next map load (the v29-v34 bug from CERULEAN on).
- Scripted trainers (no header) get their kill index at the trainer phase from v34's table (2D phase2: map, opponent,
  trainer no.); not listed = keeps D4AE/AF, which is the LAST talked-to trainer's index -> add new scripted battles there.
- **Until v29 only 23 of 322 trainer headers had a kill index**; the rest held a text pointer there, so CURSE set a bit
  somewhere in DCA4–E4A3 (box data, stack, echo of sprite tables/tile map) and nobody died from NUGGET BRIDGE on.
  New trainer data must get a kill index (killmap.py finds headers and their maps through the map text tables).
- Event flags are NOT always where pokered puts them: read the map script that checks a flag before setting it
  (v12 set D75B.7 = Cerulean Rocket thief instead of BLUE's D75A.0 until v15).
- Warping between two outdoor maps puts the player at the wrong spot; warp into a building, set wLastMap (D365),
  then walk out.
- The YES/NO box (YesNoChoice 0x362E, answer in CC26, 0 = YES) is drawn above the text box: tests must read the
  whole screen (`txt()`), not `box()`.
- Hidden/shown object toggle numbers are shifted in this ROM: read wMissableObjectList (D5CE: sprite, toggle pairs)
  on the map, flags at D5A6 + toggle/8 (Tower 7F ROCKETs + FUJI = 40–43 = D5AE bits 0–3). Tests that fake an event
  must also set its toggles, or objects that the real event hides stay in the way.
- The after-win trainer phase starts at F:46EC when GHOST (species 1F) is the Pokémon out (v18 skips it for
  GIOVANNI at SILPH 11F).
- Free space: read the manifests (offset = bank*0x4000 + addr-0x4000), not ad-hoc scans; bank 18 holds v18 7400,
  v19 7500/7A00, v20 7C00, v21 7600, v22 7D40.
- Fossil overworld sprite = 3E (Mt. Moon fossils; movement ff ff = still).
- Don't wait on the regression with `pgrep -f "run_v…sh"` from a shell: the waiter's own command line matches and it
  never ends. Run the regression with run_in_background and wait for its notification.
- Random walks for encounters must stay in the grass: use `walk_in(map, dir)` (harness) — with the real Mirage rate
  (25% since v14) a free random walk drifts into Pallet/houses and the Mirage tests fail by luck.
- New maps: use an unused map id (0x69–0x75 except 0x6C/0x71, 0xCC–0xCE, 0xED/0xEE, 0xF1–0xF4 all share a dummy
  header). Set MapHeaderPointers (0x1AE) + MapHeaderBanks (0xC23D) + MapSongBanks (3:404D); wild data (3:521C), toggles
  and the gravestone list (3:4EA2) are already empty for them. Warp-to entries = view pointer
  C6E8+7+w+(y/2)*(w+6)+x/2, y, x. Block ids of the Tower tileset: qa_ref/v19_chamber_layout.png, altar_layout.py.
  Tower blockset (1B:45C0, 176 slots): 6E-7C = chamber blocks (v20/v21), 7D-AF still unused by any map — draw rooms per
  walking tile with altar_layout_v20.py's quarter-tile method and new blocks there.
- ReplaceTileBlock (predef 18, new id in D09F) takes **b = block y, c = block x** (`ld bc` is c first in the bytes).
- After every trainer win there is a "trainer phase" (CURSE or RUN). Tests that want a normal win must RUN there.
- The base game's trainer-kill step is a second "battle" (wBattleType 3) after winning with CURSE; scripted
  trainers (no trainer header) normally get "But, it failed!" there (check at F:5033).
- Move ids are shifted at the end: A5 = the base game's CURSE, **A6 = STRUGGLE**, A7-AA = overhaul moves.
- A party mon above the badge level cap whose OT ID isn't the player's disobeys ("loafing around", naps): give
  constructed mons the player's ID (D359/D35A).
- Bank F (battle core) only has small gaps (7E0D, 7E41, 7E78, 7FB2 used by v23; 7E99, 7FC0.. 7FF8 left): put a
  5-byte stub there and the logic in 2E through v23's far-call stub; a 2E routine can redirect the battle by
  rewriting [sp+6] (the hooked return address), see build_v23.py.
- Gravestones are silent: talking to a killed trainer's grave prints nothing (the object is found, no text runs).
- Hunger engine = v30 `hunger2` (2D:5E00, via hunger_wrap): warnings at 100/50/25 steps left (DisplayTextID ids F1-F3),
  victim = nearest edible slot in front of GHOST, else below it (v32 `victim2` 2D:6080: PRETA B6 / AZHI B7 are never eaten). D469 is NOT free (bank 1 writes the animation id there every battle).
- **The v2 hunger engine eats every non-GHOST party member (and finally wipes the save) when hunger hits 0, and it does
  not check that GHOST is in the party.** Anything that takes GHOST out of the party must switch it off (v25: BLACK flag
  D46C checked in `hunger_wrap`, the home stub at 0:00E0).
- MoveSprite (0:3674) sets wJoyIgnore = FF and wStatusFlags5 bit 0 while the NPC walks; clear wJoyIgnore (CD6B) before any
  text the player must dismiss, and wait for D730 bit 0 to clear. Movement bytes: DOWN 00, UP 40, LEFT 80, RIGHT C0, end FF.
- Script-started text: `ld a,id / ldh [$ff8c],a / call DisplayTextID (294D)` uses the map's text table (header +5): add
  entries as `17 ptr bank 50` (TX_FAR) or `08 <code> c3 0425` (TX_ASM).
- Redirecting a hooked routine from a bank-2E/2D far routine: a tail-jp stub (`ld hl,R / ld b,bank / jp 3618`, 8 bytes)
  leaves the hooked code's return address at [sp+4] on entry to R (the older farcall-helper stubs: [sp+6]); R may overwrite it.
  v25 ends a battle by pointing it at F:5155; it aborts UseItem_ by pointing it at a `ret` (3:469B).
- Bank-switched far calls clobber a, b, c (Bankswitch pops the old bank into bc/a); return results through WRAM.
- Party icons (1C table at 57F2, moved to 7B9C in v25): each icon is the LEFT half (2 tiles: top T, bottom T+2) mirrored by
  OAM x-flip, frame 2 uses T+0x40. Tile ids 2C-3F and 6C-7F are free in the party menu; GetPartyMonSpriteID returns the base T.
- A test state saved under an older ROM keeps the old map-script pointer in RAM (loaded at map load): rebuild chamber/7F
  states after moving those scripts.
- Home bank has no free bytes; v25 freed 43 (0:1667-0:1691) by making UncompressMonSprite's bank choice a 2D far call.
  Bank 2D is the roomy place for code (4400-5800 used by v25, texts 5800, 7000 BLACK sprite sheet).
- New species pics need their bank: UncompressMonSprite (0:1659) picks it by species range + special cases (1F/7A
  -> 2D, B6 -> B, 15 -> 1). Bank 2D has ~15 KB free.

## Saved RAM used by the overhaul (D450–D4AD cleared on NEW GAME)
All of it is inside the saved block (wMainData D2F7–DA80); `t27_saveload.py` proves save → power cycle → CONTINUE
keeps D450–D463 and the gravestones, and NEW GAME over an old save clears them. New flags must stay in D450–D4A3 (D471–D484 = v28 NPC kill list, D430–D44F = v29 kill bits; NEW GAME clears D430–D4AD since v29).
D450 Mu answer (1 Trainer, 2 Pokémon) · D451 Ghost acquired · D452 Curse used this battle · D453 trainer
killed by Curse · D454 Mu state · D455 Ghost hunger · D456 hunger step counter · D457–D45A temp ·
D45B police alert shown this map · D45C Ghost-use counter · D45D Mirage battle active · D45E alive mask ·
D45F Ghost deposited for Mirage (1, or 2 = it was leading; v31) · D460 Mu state after Mt. Moon (0/1 introduced/2 PRETA given/3 moved to Mansion 1F) · D461 PRETA revival countdown · D462 temp: Pokémon Center heal running · D463 rival mode (0 normal/1 shock/2 hero) · D464 AGATHA quest stage (0–5) · D465 consort (1 MISTY/2 ERIKA/3 SABRINA) · D466 quest flags (bit0 failed, bit1 AGATHA gone, bit2 Mu note said). D467 ritual (0 -, 1 MR. MU battle, 2 MIRAGE phase, 3 done, 4 ????? consumed/counting steps, 5 GHOST battle, 6 BLACK done) · D468/D469 battle-hook temps · D46A step counter after the consume · D46B AGATHA talk (0 intro, 1 lore next, 2 final) · D46C BLACK (player is BLACK) · D46D/D46E last y/x · D46F Tower 7F scene (0..3) · D470 scratch (pic bank). Do not use D485–D4A3 (real game data) or D4A4–D4AF (gravestones etc.; v14 uses kill bits 26–32 = D4A7 bits 2–7, D4A8 bit 0).

## Planned (decided, not built yet)
- The RED+GHOST fusion (option A0 front/back, `overhaul/red_ghost_fusion.py`, map sprite `red_ghost_overworld.py`) is the
  player's look as BLACK since v25 (battle back picture, YOU, map walking sprite). Still RED when BLACK: the trainer-card /
  Oak-intro front picture (RedPicFront), the bike and surf map sprites. The fusion front picture (2D:41C0) is BLACK's species
  picture (species 7F, shown in the evolution scene).
- BLACK's story after the climax (destroy the POKeMON LEAGUE and consume it) is the next chapters; AGATHA only sets it up.
- The MIRAGE (random encounters, class 13, and ????? species 7A) keeps the blacked-out GENTLEMAN silhouette.

## Features (see READMEs for verified details)
v1 Oak briefing, Mr. Mu question, shaman, Ghost after rival · v2 sprites (Gentleman/Channeler), Ghost hunger
(drain, eat party, permadeath wipe), Curse frightened text, police bulletin, text fixes · v3 Mirage Black Tamer
(silhouette trainer class 13, Lv50 Fossil Kabutops/Aerodactyl, MACABREBLADE/BLACK FLAME, Ghost to PC,
player stand-in species 0x79, 65% run, permanent deaths) · v4/v5 fossil back sprites (v5 = fossilized
originals) · v6 Mr. Mu in the Cerulean trade house (Ghost route only), DOME FOSSIL question
(ACCEPT/DEFY), PRETA (Lv50 Fossil Kabutops, perfect DVs, MACABRE/CUT/SURF/STRENGTH), move A9 MACABRE
(never misses, Slash anim, leaves target at 1 HP; death-move table now at E:7D30) · v7 PRETA in party = SILPH SCOPE, whiter fossil Kabutops back, PRETA revives 2 turns
after fainting and after any battle it ended fainted · v8 fossils immune to MACABRE and PRETA not scared in Mirage
battles, Mu moves to Pokémon Mansion 1F after PRETA (placeholder lines), fossil Kabutops back = black/white only · v9 species B6 named PRETA (player's and the
Tamer's), PRETA immune to MACABREBLADE, GHOST/PRETA/fossil Aerodactyl: no Rare Candy, skipped by the Pokémon Center · v10 Mirage trainer named ?????, species B7 = AZHI (BLACK FLAME/FLY/
DRAGONBREATH/FIRE BLAST), BLACK FLAME faints the whole opposing party, new move AA DRAGONBREATH, AZHI immune to
CURSE/MACABRE/BLACK FLAME, in Mirage battles only death moves kill outright · v11 Mirage trainer pic = blacked-out GENTLEMAN, AZHI
knows DRAGON RAGE (DRAGONBREATH removed), BLACK FLAME faints only Pokémon (spares GHOST/PRETA/AZHI, never harms people) · v12 rival BLUE: CURSE can't kill him (except Champion),
"died" defeat text, shock mode (skips Cerulean/S.S. Anne/Route 22, Tower grief + bastard), Silph Co avenge/Rocket
lines, hero mode after Silph (no Route 22, Champion's ace = Lv70 MEWTWO) · v13 fixed v1 freeze after Center/Mart dialogue, GHOST taken out of the party
during the nurse's heal, fixed v12 trainer-curse register clobber (scripted trainers unkillable again) · v14 GHOST award
fix (CC49), Mirage roll uses a fresh random number (was every encounter), GHOST starts at hunger 67 (~400 steps), YOU
sent out without the Poké Ball, GENTLEMAN sprites/pic -> GAMBLER except Mr. Mu, PRETA/AZHI not in the dex, every gym
leader killable with CURSE (badge + TM from the body, gravestone, gym trainers stay active and swear revenge), killer
rumours (blamed on TEAM ROCKET) from 14 town NPCs after the first murder · v15 Nugget Bridge BLUE: killer question
+ test battle on the murder route (GHOST -> shock + "Are YOU the killer!?", no GHOST -> "gotten stronger"), BILL tells the
Lavender soul-tribe story after the S.S. TICKET, shock mode skips BLUE at Cerulean with the right flag (D75A.0) · v16 AGATHA quest part 1 (GHOST route): hostage with
FUJI on Tower 7F, relics (DOME/PRETA, AMBER/AZHI, HELIX), vessel (MASTER BALL), GHOST Lv100, consort (MISTY/ERIKA/SABRINA
takes the HELIX FOSSIL after her gym, joins AGATHA on 7F); fails on lab revival, a used MASTER BALL or all three girls dead · v17 AGATHA on FUJI's right (7F x11), the girl on
AGATHA's left (x10, FUJI's spot after the rescue), no Mr. Mu hint in her note · v18 SILPH CO. (GHOST route): Tower 7F opens the Saffron gates and clears GIOVANNI
out of the hideout; GIOVANNI's new speech, "Damn that cult...!", no trainer phase, "forces ... using you";
the PRESIDENT's MASTER BALL story (his vanished old friend) · v19 new map 0x69 TOWER CHAMBER (round room, MR. MU at the
centre) behind AGATHA on Tower 7F; stairs open from quest stage 5, AGATHA steps beside them · v20 chamber redrawn per walking tile (12x12 blocks):
one centre tile (11,11) for MR. MU, 7 new Tower blocks in slots 6E-74 · v21 ring around the centre tile, triangle of
three statues each with a gravestone in front (blocks 75-7C) · v22 a fossil sprite on each stand (OLD AMBER top,
DOME FOSSIL bottom-left, HELIX FOSSIL bottom-right). · v23 MR. MU's last talk in the chamber (successor, "I gave birth to you",
LAVENDER / BLACK TAMER, the MIRAGE = his missing half, the MASTER BALL handed back, "Is there life after death?" with no
wrong answer) and the ritual battle: party put aside (SRAM 1:B600), YOU alone with STRUGGLE, PKMN/ITEM/RUN refused,
MR. MU (class 27, species 20) never attacks and dies (gravestone, kill index 33), the MIRAGE ????? (species 7A) appears, only the MASTER BALL works and turns black when it catches; party back + ????? (or PC box). · v24 ????? keeps the MIRAGE's
blacked-out silhouette (front = the Mirage trainer pic, back = it mirrored at 32x32); the fusion is for the BLACK TAMER. · v25 the climax: ????? has a hollow-GENTLEMAN party icon; every item/Dig/Teleport/Fly is disabled in the chamber; first step out of the circle: GHOST consumes the MIRAGE (GENGAR cry placeholder), two steps later a Lv100 GHOST battle: CURSE first, ~5 s black, evolution screen "GHOST has transcended and become BLACK.", the player is BLACK (renamed, fusion back picture and map sprite, species 7F), GHOST leaves the party, hunger off; AGATHA walks up on 7F, celebrates, sends BLACK against the POKeMON LEAGUE (+ MR. MU lore, final line); the consort waits in the player's house 1F and heals. · v26 BLACK's back picture is scaled to 80% with a margin and a small halo (no more dithered square): `red_ghost_fusion.fuse_back_soft`, picture at 2D:6E00; t35 `backpic` checks the empty margin. · v27 the back picture is full size again (v26 shrank it) but shifted 2 px right / 4 px down with a small halo, so the top and sides stay clear (`red_ghost_fusion.fuse_back_shift`, picture at 2D:6F00). · v28 BLACK's world: ordinary NPCs panic and can be CURSEd on the map (gravestone, list of 10 at D471), NO = usual dialogue; Lavender/clerks/nurses/OAK/BLUE/MOM exempt; trainers don't spot BLACK. · v29 CURSE kills every trainer (299 headers got kill indices, bits D430–D44F, gravestones for all); fixes the base hack's stray RAM writes that broke the game from NUGGET BRIDGE on. · v30 GHOST hunger warnings (100 restless / 50 "<mon> seems anxious" / 25 "malicious intent"), it eats the Pokémon in front of it (below it if it leads), GENGAR's cry when it eats the player. · v31 a GHOST that led goes back to slot 1 after a MIRAGE battle (it used to come back last). · v32 GHOST never eats PRETA or AZHI (nearest edible one in front, else below, else the player); PRETA's back picture has light-grey rib lines again. · v33 PRETA's back picture shaded like its front (dark→light grey gradients inside the body along the black lines). · v34 killed trainers are gravestones right after the battle (not only after re-entering the map); the CERULEAN thief, NUGGET BRIDGE Rocket, MT. MOON Super Nerd and GAME CORNER Rocket can be killed; quiz trainers / hideout GIOVANNI fail cleanly. · v35 trainers killed from CERULEAN on vanish right away again (predef 0x13 now knows every kill); graves on re-entry as before (v34's instant graves removed).
