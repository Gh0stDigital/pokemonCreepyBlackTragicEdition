# Pokémon Creepy Black — Tragic Edition (Mu overhaul)

Binary ROM hack of the 1 MiB Game Boy ROM "Pokémon Black (Creepy)". Every version is built by a
Python script that applies **logged patches with old-byte asserts** on top of the previous verified ROM.
Never overwrite an earlier ROM; build a new version (v6, v7, …) and keep ROM length exactly 1,048,576 bytes.

## Layout
- `Creepy_Black_Mu_v1.gb` … `v23.gb` (root and `overhaul/`): builds. Latest = **v23**
  (SHA-256 04fb2d3cdb63ffe4cb3b9776da5bb12d6426d58393833d0158250e4aeadcd4d0).
- Test ROMs `Creepy_Black_Mu_vN_test.gb` (`build_vN_test.py`): vN + a built-in save (GHOST route, CHARMANDER, just after
  the POKéDEX; made by `make_save_v14.py`, packed into 2E:6000) installed when the cartridge has no save (`t29_testrom.py`).
  Keep 2E:6000–67FF free in the main builds for it. `Creepy_Black_Mu_v19…v23_chamber_test.gb` = vN + a test-only save on Tower 7F
  at AGATHA stage 5 (`make_save_v19_chamber.py`, flags set directly).
- `edit/`: original v1 handoff (v1 build.py, which needs the clean base ROM that is NOT in this repo).
- `overhaul/build_v2.py … build_v23.py`: each takes the previous version, checks its SHA, writes the next
  ROM + `manifest_vN.json` (before/after bytes per patch). READMEs: `README_v2.txt`, `README_v3.txt`, `README_v6.txt`, `README_v7.txt`, `README_v8.txt`, `README_v9.txt`, `README_v10.txt`, `README_v11.txt`, `README_v12.txt`, `README_v13.txt`, `README_v14.txt`, `README_v15.txt`, `README_v16.txt`, `README_v17.txt`, `README_v18.txt`, `README_v19.txt`, `README_v20.txt`, `README_v21.txt`, `README_v22.txt`, `README_v23.txt`.
- `overhaul/harness.py` + `t*.py`: PyBoy emulator tests. `run_all.sh` (v2 features), `run_v3.sh` (full chain
  including the Mirage tests), `run_v6.sh` (Cerulean Mu / PRETA / MACABRE; needs the chain's
  `pallet_with_ghost` state), `run_v7.sh` (v6 checks + PRETA revival / Silph Scope effect), `run_v8.sh`
  (v7 checks + Mansion Mu / PRETA in Mirage battles), `run_v9.sh` (v8 checks + PRETA vs PRETA,
  Rare Candy, Pokémon Center), `run_v10.sh` (v9 checks + AZHI / BLACK FLAME / ?????), `run_v11.sh` (same suite on v11), `run_v12.sh` (v10 suite + rival BLUE, t25_blue.py), `run_v13.sh` (v12 suite + Pokémon Center/Mart, t26_center.py), `run_v14.sh` (v13 suite + t28_v14.py: Mirage rate, YOU, dex, GAMBLER, rumours, gym leaders; `bfs_to` walks around obstacles), `run_v15.sh` (v14 suite + t30_v15.py: Nugget Bridge BLUE, BILL), `run_v16.sh` (v15 suite + t31_v16.py: AGATHA quest), `run_v17.sh` (same on v17), `run_v18.sh` (v17 suite + t32_v18.py: SILPH CO.), `run_v19.sh` (v18 suite + t33_v19.py: secret chamber), `run_v20.sh` / `run_v21.sh` (same on v20 / v21), `run_v22.sh` (+ chamber fossils), `run_v23.sh` (+ t34_v23.py: MR. MU's talk + ritual battle). Tests chain through save states in `overhaul/qa/` (gitignored; the chain
  regenerates them starting at `t1_opening.py`). Select the ROM with `CB_ROM=Creepy_Black_Mu_v5.gb`.
- Patch safety (static, no emulator): `overhaul/patchguard.py` (SM83 decoder + checks), `overhaul/patchlib.py`
  (shared build helpers: `Rom.put/data/code/hook/finish`), `overhaul/check_hooks.py` (re-checks all hooks v1-v23, found through the manifests
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

## Making a new version (v24+)
- Write `build_vN.py` with `from patchlib import *`: `Rom(input, expect_sha)`, put stubs with `rom.put`, then
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
  trainer being fought (0 = can't be killed). Killed trainers get sprite 0x49 (gravestone). Indices 0–25 base, 26–32 v14 leaders.
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
- New species pics need their bank: UncompressMonSprite (0:1659) picks it by species range + special cases (1F/7A
  -> 2D, B6 -> B, 15 -> 1). Bank 2D has ~15 KB free.

## Saved RAM used by the overhaul (D450–D4AD cleared on NEW GAME)
All of it is inside the saved block (wMainData D2F7–DA80); `t27_saveload.py` proves save → power cycle → CONTINUE
keeps D450–D463 and the gravestones, and NEW GAME over an old save clears them. New flags must stay in D450–D4A3.
D450 Mu answer (1 Trainer, 2 Pokémon) · D451 Ghost acquired · D452 Curse used this battle · D453 trainer
killed by Curse · D454 Mu state · D455 Ghost hunger · D456 hunger step counter · D457–D45A temp ·
D45B police alert shown this map · D45C Ghost-use counter · D45D Mirage battle active · D45E alive mask ·
D45F Ghost deposited for Mirage · D460 Mu state after Mt. Moon (0/1 introduced/2 PRETA given/3 moved to Mansion 1F) · D461 PRETA revival countdown · D462 temp: Pokémon Center heal running · D463 rival mode (0 normal/1 shock/2 hero) · D464 AGATHA quest stage (0–5) · D465 consort (1 MISTY/2 ERIKA/3 SABRINA) · D466 quest flags (bit0 failed, bit1 AGATHA gone, bit2 Mu note said). D467 ritual (0 -, 1 MR. MU battle, 2 MIRAGE phase, 3 done) · D468/D469 battle-hook temps. Do not use D485–D4A3 (real game data) or D4A4–D4AF (gravestones etc.; v14 uses kill bits 26–32 = D4A7 bits 2–7, D4A8 bit 0).

## Planned (decided, not built yet)
- The random Mirage encounters' trainer pic (class 13, still v11's blacked-out GENTLEMAN at 13:7FA5) -> the RED+GHOST
  fusion (option A0) that v23 already uses for the caught ????? (species 7A): trainer pics must be in bank 13, which is
  full, so this needs a hook in the trainer-pic loader. Fusion maker: `overhaul/red_ghost_fusion.py`
  (`fuse(rom, small='A0')` front, `fuse_back(rom)` back; references `qa_ref/black_tamer_pic*.png`, `black_tamer_back*.png`).

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
MR. MU (class 27, species 20) never attacks and dies (gravestone, kill index 33), the MIRAGE ????? (species 7A, fusion
pics) appears, only the MASTER BALL works and turns black when it catches; party back + ????? (or PC box).
