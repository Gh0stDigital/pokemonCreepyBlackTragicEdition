# Pokémon Creepy Black — Tragic Edition (Mu overhaul)

Binary ROM hack of the 1 MiB Game Boy ROM "Pokémon Black (Creepy)". Every version is built by a
Python script that applies **logged patches with old-byte asserts** on top of the previous verified ROM.
Never overwrite an earlier ROM; build a new version (v6, v7, …) and keep ROM length exactly 1,048,576 bytes.

## Layout
- `Creepy_Black_Mu_v1.gb` … `v89.gb` (root and `overhaul/`): builds. Latest = **v89**
  (SHA-256 c65fefc4232baeec861e26d91fef50cfcd59b713cce9aa1e320a8f32b14e6def).
- Test ROMs `Creepy_Black_Mu_vN_test.gb` (`build_vN_test.py`): vN + a built-in save (GHOST route, CHARMANDER, just after
  the POKéDEX; made by `make_save_v14.py`, packed into 2E:6000) installed when the cartridge has no save (`t29_testrom.py`).
  Keep 2E:6000–67FF and 1:7E00–7E0F free in the main builds for it. `Creepy_Black_Mu_v19…v50_chamber_test.gb` = vN + a test-only save on Tower 7F
  at AGATHA stage 5 (`make_save_v19_chamber.py`, flags set directly). `Creepy_Black_Mu_v25_ritual_test.gb` / `v26…v50_ritual_test.gb` = a save in the
  TOWER CHAMBER right after MR. MU's ritual (????? in the party): `make_save_v25_ritual.py` plays the ritual in the emulator
  and saves through the START menu; walking out of the circle starts the v25 climax.
- `edit/`: original v1 handoff (v1 build.py, which needs the clean base ROM that is NOT in this repo).
- `overhaul/build_v2.py … build_v50.py`: each takes the previous version, checks its SHA, writes the next
  ROM + `manifest_vN.json` (before/after bytes per patch). READMEs: `README_v2.txt`, `README_v3.txt`, `README_v6.txt`, `README_v7.txt`, `README_v8.txt`, `README_v9.txt`, `README_v10.txt`, `README_v11.txt`, `README_v12.txt`, `README_v13.txt`, `README_v14.txt`, `README_v15.txt`, `README_v16.txt`, `README_v17.txt`, `README_v18.txt`, `README_v19.txt`, `README_v20.txt`, `README_v21.txt`, `README_v22.txt`, `README_v23.txt`, `README_v24.txt`, `README_v25.txt`, `README_v26.txt`, `README_v27.txt`, `README_v28.txt`, `README_v29.txt`, `README_v30.txt`, `README_v31.txt`, `README_v32.txt`, `README_v33.txt`, `README_v34.txt`, `README_v35.txt`, `README_v36.txt`, `README_v37.txt`, `README_v38.txt`, `README_v39.txt`, `README_v40.txt`, `README_v41.txt`, `README_v42.txt`, `README_v43.txt`, `README_v44.txt`, `README_v45.txt`, `README_v46.txt`, `README_v47.txt`, `README_v48.txt`, `README_v49.txt`, `README_v50.txt` … `README_v89.txt`.
- `overhaul/harness.py` + `t*.py`: PyBoy emulator tests. `run_all.sh` (v2 features), `run_v3.sh` (full chain
  including the Mirage tests), `run_v6.sh` (Cerulean Mu / PRETA / MACABRE; needs the chain's
  `pallet_with_ghost` state), `run_v7.sh` (v6 checks + PRETA revival / Silph Scope effect), `run_v8.sh`
  (v7 checks + Mansion Mu / PRETA in Mirage battles), `run_v9.sh` (v8 checks + PRETA vs PRETA,
  Rare Candy, Pokémon Center), `run_v10.sh` (v9 checks + AZHI / BLACK FLAME / ?????), `run_v11.sh` (same suite on v11), `run_v12.sh` (v10 suite + rival BLUE, t25_blue.py), `run_v13.sh` (v12 suite + Pokémon Center/Mart, t26_center.py), `run_v14.sh` (v13 suite + t28_v14.py: Mirage rate, YOU, dex, GAMBLER, rumours, gym leaders; `bfs_to` walks around obstacles), `run_v15.sh` (v14 suite + t30_v15.py: Nugget Bridge BLUE, BILL), `run_v16.sh` (v15 suite + t31_v16.py: AGATHA quest), `run_v17.sh` (same on v17), `run_v18.sh` (v17 suite + t32_v18.py: SILPH CO.), `run_v19.sh` (v18 suite + t33_v19.py: secret chamber), `run_v20.sh` / `run_v21.sh` (same on v20 / v21), `run_v22.sh` (+ chamber fossils), `run_v23.sh` (+ t34_v23.py: MR. MU's talk + ritual battle), `run_v24.sh` (+ t34 sendout: ????? back pic), `run_v25.sh` (+ t35_v25.py: items/icon/climax/sprites/you/agatha/house/normal; its chamber states are cached in `qa/*v25a*`, delete them when the chamber/7F code layout changes), `run_v28.sh` (+ t36_v28.py: NPC panic/curse, exempt NPCs, trainer sight; t37_kills_save.py), `run_v29.sh` (+ t38_v29.py: kill system), `run_v30.sh` (+ t39_v30.py: hunger warnings/victim/GENGAR), `run_v31.sh` (+ t40_v31.py: GHOST back to slot 1 after a MIRAGE), `run_v32.sh` (+ t41_v32.py: PRETA/AZHI never eaten, PRETA back shading), `run_v33.sh` (+ t42_v33.py: PRETA back shaded like its front), `run_v34.sh` (+ t43_v34.py: gravestone right after the battle; v34 only), `run_v35.sh` (v33 suite + t44_v35.py: killed trainers vanish at once), `run_v36.sh` (v35 suite + t45_v36.py: 7F/gym START menu, AGATHA Lv50, GHOST level cap, GIOVANNI defeat line, BLUE after SILPH), `run_v37.sh` (v36 suite on v37; t35 backpic checks the visible 28x28), `run_v38.sh` (v37 suite + t46_v38.py: BLACK party member), `run_v39.sh` (v38 suite + t47_v39.py: BANE in battle), `run_v40.sh` (v39 suite + t48_v40.py: BANE on the map), `run_v41.sh` (v40 suite + t49_v41.py: CONSUME), `run_v42.sh` (v41 suite + t50_v42.py: BANEd NPC's ball stays put), `run_v43.sh` (v42 suite + t51_v43.py: black ball graphics), `run_v44.sh` (v43 suite + t52_v44.py: LEAGUE as BLACK, MOON STONE), `run_v45.sh` (v44 suite + t53_v45.py: BLUE replaces CURSEd POKeMON), `run_v46.sh` (v45 suite + t54_v46.py: seven changes), `run_v47.sh` (v46 suite, t49 skipped + t55_v47.py: METAMORPHOSIS, black POKeMON, CURSE eats), `run_v48.sh` (v47 suite + t56_v48.py: GHOST WALK, DAMNATION, negative animations, AZHI), `run_v49.sh` (v48 suite + t57_v49.py: scared POKeMON, status immunity, Tower, services), `run_v50.sh` (v49 suite + t58_v50.py: PRETA/AZHI nervous, anxious, revival, levels), `run_v51.sh` … `run_v53.sh` (+ t59-t61), `run_v54.sh` (v53 suite + t62_v54.py: MOM among the channelers), `run_v55.sh` (+ t63_v55.py: LORELEI's speeches as BLACK, no dialogue after, door opens by itself), `run_v56.sh` (+ t64_v56.py: BRUNO's speeches as BLACK, same pattern), `run_v57.sh` (+ t65_v57.py: LANCE's speeches as BLACK; his after text also set D866 bit 6, now set by the tail), `run_v58.sh` (+ t66_v58.py: BLUE as BLACK, no Oak / Hall of Fame, AGATHA's scene in the Hall of Fame; D876 = stage), `run_v59.sh` (+ t67_v59.py: OAK'S LAB empty but for the hiding aide; D876 5 = told where OAK went), `run_v60.sh` (+ t68_v60.py: BILL's cottage scene and battle; D877 = sub-stage, D876 6 = OAK at CERULEAN CAVE), `run_v61.sh` (+ t69_v61.py: BILL's six POKeMON and the PSYCHIC picture), `run_v62.sh` (+ t70_v62.py: CERULEAN CAVE, PROF. OAK scene / battle / ending with the credits and the LAVENDER theme; bank 31 holds the v62 code), `run_v63.sh` (+ t71_v63.py: the ten SHAMANESSES in the towns; bank 31 5000 = app63/wrap63), `run_v64.sh` (+ t72_v64.py: secret door in the HALL OF FAME corner (y1,x0) to the League lobby; object data AND the warp-to list that follows it live at 16:65D6), `run_v65.sh` (+ t73_v65.py: MR. MU's first meeting in PALLET: frozen player, new nameless speech, he waits, gone after the next building; the Pallet script is bank 31 6000 pal65), `run_v66.sh` (+ t74_v66.py + `check_sets.py`: sprite-set check incl. position-dependent routes; PALLET shamaness replaces the placeholder; bank 31 6600 app66/wrap66, 6400 pal66, texts 6A00), `run_v89.sh` (+ t97_v89.py: ROUTE 22's first rival fight (opponent E1): v12's class-wide hooks already give shock mode + GHOST's hesitation; r22a89 (14:6BA0, text-1 chooser, table entry 14:5175) says the shock speech after he runs away when D452 (CURSE used), else the original 14:51B2), `run_v88.sh` (+ t96_v88.py: PROF. OAK's end: anim88/end88 (31:5C00) switch hTileAnimations ($FFD7) off at the start of scene62 / ending62 - the cave's water tile (VRAM $9140) overwrote tile 20 of the picture drawn at $9000 - and end88 hides the player's sprite (its white OAM entries covered credit letters); shat88 (2F:5E00) = no second MOON STONE text in the after-win pass (d05a = 3)), `run_v87.sh` (+ t95_v87.py: BILL ends the walk at (6,2) facing down and is hidden (HideObject = predef 11, toggle 62) when the battle starts (bill87 30:4540); app87 31:5B00 restores the object pictures of the player's house / BILL's cottage before the sprite loader; LAVENDER music in the house (music51 maps < $26); CERULEAN cave guard (city object 10, toggle 8 = D5A7 bit0) hidden when BLUE is beaten as BLACK (s3_87 1D:7FA0, cer87 06:7100)), `run_v86.sh` (+ t94_v86.py: Route 22 gate also for BLACK (gate86 14:6B60), no fanfare after League/BLUE/OAK/BILL (vict86 bank 32 5200, class list), Hall of Fame silent (music86), GHOST WALK power 20+level*1.5 (gpow86), BLUE hidden at once (s3_86 1D:7F80) + AGATHA faces up (hof86 30:4500), OAK LAB: app86 31:5AA0 restores the object pictures before the sprite loader (aide drew BLUE's tiles) + aide86 METAMORPHOSIS question (bank 32 5400, ext86 7:7FE0)), `run_v85.sh` (+ t93_v85.py names: the player name becomes BLACK on the first League room as BLACK and STAYS (name85 2E:5D00, backup D879-D883, flag D884)), `run_v84.sh` (+ t91_v84.py / t92_v84.py: ball84 (2F:5C00) picks a slot no other sprite uses for the black ball - item balls are ALWAYS in slot 0B, gravestones/boulders in 0C; dam84 = DAMNATION faints visibly; msg84/slide84 = BLACK slides in on a switch; ch84 (30:6F00) no channelers on 7F after the ritual; name84 (2E:5C00, replaced by name85 in v85) player name BLACK in the LEAGUE rooms F5-F7 + 71; shat84 (F:5046 stub) MOON STONE shatters at the last faint; rdisp84 (31:5A80) keeps v80's scared lines out of story maps), `run_v83.sh` (+ t90_v83.py: METAMORPHOSIS on a trainer's POKeMON = CURSE kill (CC39 = 1, D452 = 1 via meta83 31:5900, no "fainted!", frightened trainer line, sulk/notoriety); black pictures solid (fill83 31:5980: holes enclosed on all four sides filled)), `run_v82.sh` (v81 suite; t47/t48 expect "<MON> was ensnared!" from v82: the add-POKeMON texts are TX_FAR to bank 31:5800), `run_v81.sh` (+ t89_v81.py: GHOST WALK: back picture after turn 2 (AnimationShowMonPic via anim81, bank 31:5700), field move in BLACK's party menu (D878 = ghost walk on: inverted screen via home core81 0:35BF / vbl81 0:1251 / shortened LoadGBPal 0:20E7, no encounters via tow81 4:7BD0, field tables at 1:7E60, fm81 4:7BDC)), `run_v80.sh` (+ t88_v80.py: as BLACK ordinary alive trainers speak scared before and after the battle; bank 31 4C00 rdisp80 -> rdisp69, texts 31:5000), `run_v79.sh` (+ t87_v79.py: 7F after the ritual: app75 now runs at every stage 5 (lpic75 obj 15 = MOM 33), MOM hidden in the house when BLACK (house79 12:7200)), `run_v78.sh` (+ t86_v78.py: evolution RED -> GHOST -> BLACK (evo78 2D:4B60, the 1E:7E34 animation twice), GHOST always leaves the party at the end of the climax), `run_v77.sh` (+ t85_v77.py: chamber silent until BLACK (music77 30:4400), MR. MU's quiet start (pre77), victory fanfare guard (vicw77/vict77), fossils until RIT 6, climax turn order: D467 5 -> 7 (player's turn) -> 8 -> 5 (cm77 2D:4B0E, et77, menu77 2E:7820)), `run_v76.sh` (+ t84_v76.py: no encounters on TOWER 7F (tow76 4:7BC0); chamber stands: HELIX top (y7 x11), DOME left (y15 x6), AMBER right (y15 x16) = objects 4 / 3 / 2), `run_v75.sh` (+ t83_v75.py: TOWER 7F channelers after a menu redraw; app75 bank 31:4B00 restores objects 4-15's list pictures before InitMapSprites' body), `run_v74.sh` (+ t82_v74.py: CINNABAR/town signs, GAME CORNER Rocket silent when killed (and his walk skipped), gravestones stand still (killed74 2D:6220), MANSION 1F statue switch vs MR. MU (text 4 stub 11:7519); shamaness marker = pic 19 + byte0 D0 + text byte = her slot, code bank 31:4900 app74/wrap74, gc stub 12:7140), `run_v73.sh` (+ t81_v73.py: PRETA unveil text, FUJI/AGATHA lines, Saffron shamaness at (24,32), SNORLAX skip after CURSE; stubs 16:6800, 7:772B, texts bank 32:5000), `run_v72.sh` (+ t80_v72.py: SNORLAX/balls/gravestones, VRAM slot sweep; set 12 reordered, ROUTE 12 south = set 8, picture lookup 5:7A05 -> 5:7F9C/7FF1 hides a missing gravestone), `run_v71.sh` (+ t79_v71.py: NOTORIETY D85C (+1 per trainer battle won with CURSE used and the trainer alive; D85E bit0 kill marker, bit1 counted; kill marker set in 2E:41db, cleared at battle start 14:6a50, counted in 2D:5fc0 hook) and the Saffron gate guards (ROUTE 5/6/7/8 gate houses: fee 100 x notoriety up to 6000, new text id 4 per gate, bank 32 holds the bribe code/texts, paid flag D85D cleared by every map load via the 2E:4000 chain), `run_v70.sh` (+ t78_v70.py: killed NUGGET BRIDGE Rocket / CERULEAN thief don't talk after the battle (kill bits in D44F), their flags still fire; stubs 14:7100 / 06:7000), `run_v69.sh` (+ t77_v69.py: ordinary trainers sulk after CURSE+spare (16 lines by kill index; sulk bits in unused event-flag bytes D784.. see README_v69; D844 = header trainer fighting); fixes the v67 loss of the beaten flag), `run_v68.sh` (+ t76_v68.py: MIRAGE chance = victims*164/256 (D45C), cap 64 at 100 victims, none as BLACK; roll patched at 2E:4310 -> m68 2E:4280), `run_v67.sh` (+ t75_v67.py: gym SHOCK mode: D839 shock bits, D83A-D83F sulk bits, D842 armed gyms; home stub 0:00CE far-calls bank 31 7000 rdisp, EndTrainerBattle far-calls r2). `Creepy_Black_Mu_vN_mysave_test.gb` = vN + the user's own save (`Creepy_Black_Mu_user.sav`); `_mysave2_test.gb` = the user's second save (`Creepy_Black_Mu_user2.sav`, Cerulean); `_mysave3_test.gb` = third save (`Creepy_Black_Mu_user3.sav`, Tower 7F, AGATHA stage 3, bag full). `_mysave4_test.gb` = fourth save (`Creepy_Black_Mu_user4.sav`, HALL OF FAME as BLACK, D876 = 4: the player stuck there; v64's secret door is the way out; built for v64 by `build_v64_mysave4_test.py`). Tests chain through save states in `overhaul/qa/` (gitignored; the chain
  regenerates them starting at `t1_opening.py`). Select the ROM with `CB_ROM=Creepy_Black_Mu_v5.gb`.
- Assembler: `overhaul/sm83asm.py` (SM83 assembler built from `ref/instruction_set.py`: labels, `.local` labels, db/dw/ds,
  `farcall addr,bank` macro; `test_sm83asm.py` round-trips real ROM code byte for byte). v25's code is written in it.
- Patch safety (static, no emulator): `overhaul/patchguard.py` (SM83 decoder + checks), `overhaul/patchlib.py`
  (shared build helpers: `Rom.put/data/code/hook/finish`), `overhaul/check_hooks.py` (re-checks all hooks v1-v72, found through the manifests
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

## Making a new version (v51+)
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
- Outdoor maps can only show sprites in their sprite set (Pallet = set 1 at 0x17AB9). **Routes pick their set by position (5:7A89: axis, threshold, set A, set B) and share the town sets: never overwrite a set entry without `check_sets.py` (v63's channeler edit broke three routes' NPCs until v66).**
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
- Move ids are shifted at the end: A5 = the base game's CURSE, **A6 = STRUGGLE**, A7-AC = overhaul moves (data of A7+ at
  E:7D30 + (id-A7)*6, room up to AE before E:7D60; animation ids A6+ are special animations, so every overhaul move is
  mapped to another move's animation in 2F anim48).
- A party mon above the badge level cap whose OT ID isn't the player's disobeys ("loafing around", naps): give
  constructed mons the player's ID (D359/D35A).
- Bank F (battle core) only has small gaps (7E0D, 7E41, 7E78, 7FB2 used by v23; 7E99, 7FC0.. 7FF8 left): put a
  5-byte stub there and the logic in 2E through v23's far-call stub; a 2E routine can redirect the battle by
  rewriting [sp+6] (the hooked return address), see build_v23.py.
- Overhaul map scripts hide objects by writing picture ID 0 (C1x0) + position FF. Since v36 LoadMapSpriteTilePatterns
  (5:7871, rerun on every redraw after a menu) skips picture 0; before that it loaded a "sheet" for picture 0 from the
  bytes in front of SpriteSheetPointerTable (bank 41, 255 tiles) over the map tiles (Tower 7F/gyms garbage after START).
- The battle engine prints "NAME:" in front of a trainer's end-battle (defeat) text: never start one with the name
  (v18's GIOVANNI line showed "GIOVANNI: GIOVANNI:" until v36); start on line 2 like v2's frightened texts.
- The battle screen shows only the top-left **28x28** of a 32x32 back picture (7x7 tiles): keep the player's back
  picture (and any halo) inside it (v27's BLACK picture was cut off on the right and bottom until v37).
- Changing an NPC's picture doesn't stop it: wandering NPCs have movement byte 1 (C2x6) = $FE (WALK), reloaded from the
  map data at every map load; set $FF (STAY) for anything that must stand still (v42 black balls). Tests' freeze() hides this.
- Outdoor maps load only their sprite set: a picture outside the set gets a garbage VRAM slot (InitOutsideMapSprites' lookup
  runs past wSpriteSet) and is drawn with other sprites' tiles. Four-tile (still) slots: 0B = $8780, 0C = $87C0 (below the font
  at $8800); v43 ball_fix puts the ball there after every InitMapSprites (5:785B -> 5:7FB0). Check new map sprites on screen.
- A wrapper around a game routine must return exactly what the routine returned: InitMapSprites returns carry set on
  outdoor maps and MIRAGE code depends on it; v43's first build tail-called a far routine there (carry/registers lost)
  and the game reset after every MIRAGE battle (caught by t40). Push af/bc/de/hl around the far call.
- Battle move menu: wCurrentMenuItem (CC26) is 1-based while the menu is open (the game decrements it before storing the
  move at F:545D); a refused move goes back through F:546D (redraw + MoveSelectionMenu, the "no PP" path). Elite Four
  class ids: LORELEI 2C, BRUNO 21, AGATHA 2E, LANCE 2F. Switching the player's POKeMON from code: set wWhichPokemon
  (CF92) AND wBattleMonSpecies2 (CFD9) / wcf91 before SwitchPlayerMon (F:5279), or the old back picture stays.
- Trainer parties: TrainerDataPointers E:5D79 (index class-1; RIVAL3's moved to E:7D60 by v12), ReadTrainer's AddPartyMon calls
  E:5CCF/E:5CE6 (v45 hooks them), EvosMovesPointerTable E:70D1, internal->dex table 0x4102E. Unused saved bytes: v45 found
  event-flag bytes with no code operand / trainer-header reference (D86A-D877, D839-D846, ...) - check again before using more.
- Battle start send-out: F:41D4 slide (v46 pre46) and SendOutMon F:4CBC message far call (v46 msg46); drawing a back
  picture without the grow animation = predef 2 (AnimateSendingOutMon) with wIsInBattle = 0, hl = $C480 (YOU's way).
  Tests that sample VRAM between long button waits miss short pictures (BANE ball): hook the routine instead.
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
- Home far stubs since v38: the unused bytes after the RST vectors (0x01-0x07, 0x11-0x17, 0x19-0x1F, 0x21-0x27 used; 0x29 = v39 bane_move; 0x39 = v44 sel44; 0x31 = v40 trampoline
  `ldh [hLoadedROMBank],a / ld [$2000],a / jp hl` (switch bank and jump, caller's stack kept); none left after 0x39; 0x09 = shared `jp Bankswitch`; since v49 0x08 = 00, so `ld hl,addr / ld b,bank / rst 08` is a 6-byte far call (flags survive, a/b/c don't)): `21 lo hi 06 bank 18 xx` (7 bytes) per stub. No code executes RST 00-38.
- **Banks 2F-3F are completely empty** (the game never used them): v39+ code lives in 2F.
- AddPartyMon (0:395B) with wMonDataLocation (CC49) = $10 adds to the player's party WITHOUT the nickname prompt (naming only when
  CC49 == 0; party/enemy choice uses the low nibble). It reuses the name buffer CD6D: call GetMonName (0:2FCF) after it.
- Far calls lose register b too: a routine that returns its result in b (LearnMove 1:6E3C: b = 1 learned) must be checked
  some other way when far-called (v41 looks at BLACK's move list).
- AddNTimes is 0:3ABB in this ROM (0:3A87 is vanilla Red's address = a different routine here: v38's first build crashed).
- **Code in a switched bank must not write the MBC bank register ($2000) itself** (the next opcode is fetched from the new bank): bank-switch through the home trampoline 0:0031 (a = bank, hl = target, hl is clobbered) or Bankswitch (3618: far call, a/b/c/hl clobbered, d/e/flags survive). ReadTrainerHeaderInfo (0:31C4) reads the header from the *mapped* bank. v67's home 0:00CE is a 18-byte stub (far call to rdisp).
- Home bank has no free bytes; v25 freed 43 (0:1667-0:1691) by making UncompressMonSprite's bank choice a 2D far call.
  Bank 2D is the roomy place for code (4400-5800 used by v25, texts 5800, 7000 BLACK sprite sheet).
- New species pics need their bank: UncompressMonSprite (0:1659) picks it by species range + special cases (1F/7A
  -> 2D, B6 -> B, 15 -> 1). Bank 2D has ~15 KB free.

- **DisplayTextID takes a text id <= wNumSprites for a SPRITE and looks the text up in that sprite's text byte (D4E4+2*(n-1)+1).** A sign / hidden event whose id is <= the sprite count is hijacked: v63's shamaness (appended as the last sprite, text byte 3F) broke the first sign of five towns ("C3 ERROR.") until v74; v8's MR. MU (object 4) hijacked the MANSION 1F statue switch (hidden event arg 4) until v74. Appending an object shifts which ids are "sprites": check every sign/hidden-event id of the map. Sprites only move while on screen (image index != FF), and a hidden (killed) sprite never finishes a MoveSprite walk: scripts that wait on D730 bit 0 freeze; tests must stand near a walker to see it walk.

- **InitMapSprites (re-run on every redraw) assigns VRAM slots from the sprites' pictures AT THAT MOMENT but a redraw does not copy the tiles again: any overhaul code that hides objects with picture 0 (ch53 on Tower 7F) must give the object-list pictures back before the loader runs (v75 app75), or slots shift and sprites draw other pictures' tiles / vanish.**

## Saved RAM used by the overhaul (D450–D4AD cleared on NEW GAME)
All of it is inside the saved block (wMainData D2F7–DA80); `t27_saveload.py` proves save → power cycle → CONTINUE
keeps D450–D463 and the gravestones, and NEW GAME over an old save clears them. New flags must stay in D450–D4A3 (D471–D484 = v28 NPC kill list (sprite|$80 = BANEd since v40), D86A–D874 = v45 BLUE's replacements (one byte per BLUE line; unused event-flag bytes), D722–D727 = v40 waiting black balls (2 x map, sprite, species; unused WRAM, not cleared on NEW GAME), D430–D44F = v29 kill bits; NEW GAME clears D430–D4AD since v29).
D450 Mu answer (1 Trainer, 2 Pokémon) · D451 Ghost acquired · D452 Curse used this battle · D453 trainer
killed by Curse · D454 Mu state · D455 Ghost hunger · D456 hunger step counter · D457–D45A temp ·
D45B police alert shown this map · D45C Ghost-use counter · D45D Mirage battle active · D45E alive mask ·
D45F Ghost deposited for Mirage (1, or 2 = it was leading; v31) · D460 Mu state after Mt. Moon (0/1 introduced/2 PRETA given/3 moved to Mansion 1F) · D461 PRETA revival countdown · D462 temp: Pokémon Center heal running · D463 rival mode (0 normal/1 shock/2 hero) · D464 AGATHA quest stage (0–5) · D465 consort (1 MISTY/2 ERIKA/3 SABRINA) · D466 quest flags (bit0 failed, bit1 AGATHA gone, bit2 Mu note said). D467 ritual (0 -, 1 MR. MU battle, 2 MIRAGE phase, 3 done, 4 ????? consumed/counting steps, 5 GHOST battle, 6 BLACK done; v77: 7 = the player's turn in the GHOST battle pending, 8 = played) · D468/D469 battle-hook temps · D46A step counter after the consume · D46B AGATHA talk (0 intro, 1 lore next, 2 final) · D46C BLACK (player is BLACK) · D46D/D46E last y/x · D46F Tower 7F scene (0..3) · D470 scratch (pic bank). Do not use D485–D4A3 (real game data) or D4A4–D4AF (gravestones etc.; v14 uses kill bits 26–32 = D4A7 bits 2–7, D4A8 bit 0).

- **A far call (rst 08 / Bankswitch) destroys hl: v67's EndTrainerBattle hook lost the trainer-flag address in hl, so no trainer was marked beaten (v67/v68). Push hl in the home code and read it from the stack in the far routine ([sp+6] at entry through `rst 08`); tests must not set game flags by hand where the code under test is supposed to set them.**

- Bank 32 (v71) holds new code; bank 7 free space 7619+ (gate stubs); 2D:4a00 notoriety hook; 2E:42b0/42d0 map-load and kill chains. The text engine's TX_BCD (`02 lo hi flags`) printed NOTHING in v71's first try: fee texts are pre-rendered per amount instead.

- **Outdoor sprite sets: entries 1-9 = walkers (<$3D), entries 10-11 = the two four-tile pictures (>= $3D); an object's VRAM slot = its picture's position in the set + 1 (5:79F4 lookup), the loader puts the 1st/2nd four-tile picture at $8780/$87C0 whatever their position. A four-tile picture anywhere else draws other sprites' tiles (v1-v71: SNORLAX in set 12; the item balls on routes 13-17 looked like Snorlax). Never add a third four-tile picture to a set (only two slots): check_sets.py fails on a wrong order. Position-split maps keep the set chosen at the last FULL reload (map load / battle); a redraw after a menu or text skips the tile copy (wFontLoaded bit 0).**

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
FUJI on Tower 7F, relics (DOME/PRETA, AMBER/AZHI, HELIX), vessel (MASTER BALL), GHOST Lv100 (Lv50 since v36), consort (MISTY/ERIKA/SABRINA
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
blacked-out silhouette (front = the Mirage trainer pic, back = it mirrored at 32x32); the fusion is for the BLACK TAMER. · v25 the climax: ????? has a hollow-GENTLEMAN party icon; every item/Dig/Teleport/Fly is disabled in the chamber; first step out of the circle: GHOST consumes the MIRAGE (GENGAR cry placeholder), two steps later a Lv100 GHOST battle: CURSE first, ~5 s black, evolution screen "GHOST has transcended and become BLACK.", the player is BLACK (renamed, fusion back picture and map sprite, species 7F), GHOST leaves the party, hunger off; AGATHA walks up on 7F, celebrates, sends BLACK against the POKeMON LEAGUE (+ MR. MU lore, final line); the consort waits in the player's house 1F and heals. · v26 BLACK's back picture is scaled to 80% with a margin and a small halo (no more dithered square): `red_ghost_fusion.fuse_back_soft`, picture at 2D:6E00; t35 `backpic` checks the empty margin. · v27 the back picture is full size again (v26 shrank it) but shifted 2 px right / 4 px down with a small halo, so the top and sides stay clear (`red_ghost_fusion.fuse_back_shift`, picture at 2D:6F00). · v28 BLACK's world: ordinary NPCs panic and can be CURSEd on the map (gravestone, list of 10 at D471), NO = usual dialogue; Lavender/clerks/nurses/OAK/BLUE/MOM exempt; trainers don't spot BLACK. · v29 CURSE kills every trainer (299 headers got kill indices, bits D430–D44F, gravestones for all); fixes the base hack's stray RAM writes that broke the game from NUGGET BRIDGE on. · v30 GHOST hunger warnings (100 restless / 50 "<mon> seems anxious" / 25 "malicious intent"), it eats the Pokémon in front of it (below it if it leads), GENGAR's cry when it eats the player. · v31 a GHOST that led goes back to slot 1 after a MIRAGE battle (it used to come back last). · v32 GHOST never eats PRETA or AZHI (nearest edible one in front, else below, else the player); PRETA's back picture has light-grey rib lines again. · v33 PRETA's back picture shaded like its front (dark→light grey gradients inside the body along the black lines). · v34 killed trainers are gravestones right after the battle (not only after re-entering the map); the CERULEAN thief, NUGGET BRIDGE Rocket, MT. MOON Super Nerd and GAME CORNER Rocket can be killed; quiz trainers / hideout GIOVANNI fail cleanly. · v35 trainers killed from CERULEAN on vanish right away again (predef 0x13 now knows every kill); graves on re-entry as before (v34's instant graves removed). · v36 GHOST max level 50 (exp capped in GainExperience; above 50 = frozen), AGATHA's quest needs GHOST Lv50; the START menu no longer garbles Tower 7F / the girls' gyms (sprite loader skips hidden picture 0); GIOVANNI's SILPH defeat line without the doubled name; BLUE after SILPH (GHOST route): doesn't understand what you've become, vows to overcome your dark power. · v37 BLACK's back picture (same silhouette + halo) scaled to fit the visible 28x28 of the battle screen (v27's was cut off). · v38 BLACK TAMER as a party member: evolution scene RED -> BLACK TAMER (species 86 = RED's picture), trainer card picture, BLACK (7F, Lv1, perfect DVs, Lv10 stats) + PRETA + AZHI join at the ritual; BLACK can't faint (1 HP), no battle exp, no items, no PC/Day Care, no rename, poison can't kill it. · v39 BANE (move AA) in battle: a POKeMON (wild or a trainer's) is taken into the party/box behind a black screen, its cry and a black POKe BALL; after a trainer battle BANE kills the trainer and turns them into a random uncaught POKeMON that joins. · v40 BANE on the map: "BANE them?" -> black screen, cry of a random uncaught POKeMON, the NPC is a black POKe BALL (sprite 47) to pick up (Lv 5+5/badge, party or box); BANEd NPCs vanish (no gravestone); 2 balls can wait. · v41 CONSUME (BLACK's party-menu entry): eat a party member (not PRETA/AZHI), take one of its moves (LearnMove, BANE unforgettable), gain its experience; stats at level + 9. · v42 a BANEd NPC's black ball can't move (movement byte C2x6 = STAY per frame and at map load; v40 left WALK and the ball wandered). · v43 the black ball = the battle-throw POKe BALL blacked out; it now really shows on outdoor maps (four-tile slot 0B/0C + tiles copied after every InitMapSprites). · v44 POKeMON LEAGUE as BLACK part 1: LORELEI/BRUNO/LANCE (MOON STONE): CURSE/MACABREBLADE/BLACK FLAME/MACABRE/BANE refused (flash, "A strange power blocks the move ...", trainer's line), after their last POKeMON "The MOON STONE shatters!", BLACK is sent out, BANE mandatory in the phase (else AGATHA's words); AGATHA's room empty. · v45 BLUE replaces every POKeMON line the player CURSEs (any rival battle) with a random one of the original 149 (no MEW/MEWTWO, none of his lines, no duplicates), same level, evolved for that level; saved at D86A. BLUE's final battle as BLACK next. · v46 AGATHA's shell line about its energy (no "my people"); BLACK leading a battle is simply there (no slide/"Go!"/animation); BANE ball in battle = throw ball, fully black; map ball = item ball, fully black; GHOST Lv100 right after consuming the MIRAGE; CONSUME without taking a move (B); no badge checks at the LEAGUE gates as BLACK (scared guards). · v47 (redux 1) BANE renamed METAMORPHOSIS (THUNDERBOLT animation in battle), POKeMON gained by it are pitch black (back picture, status screen, party icon; marked by struct byte 7 = 1), CONSUME replaced by the party-menu CURSE (eats, experience only, no move), BLACK's moves fixed (METAMORPHOSIS, CURSE; full PP every step). · v48 (redux 2) GHOST WALK (AB, FLY-like, TELEPORT/CUT animations inverted), DAMNATION (AC, HYPER BEAM animation, CURSE + the whole trainer team dies), MACABRE = CRABHAMMER and BLACK FLAME = FIRE BLAST animations in a negative palette (2F inv48 via 1E:4D65/4D98), AZHI knows SKY ATTACK instead of FIRE BLAST. · v49 (redux 3) POKeMON too scared to attack BLACK (except MOON STONE / MIRAGE / PRETA / AZHI), status immunity (BLACK all, PRETA/AZHI all but burn/freeze), no POKeMON TOWER encounters as BLACK, nurses/clerks/prize vendor/coin clerk/bike shop/MAGIKARP salesman/DAY CARE/NAME RATER/trades/fossil revival refuse BLACK. · v50 (redux 4) PRETA halves the defense of non-GHOST foes (physical damage x2), AZHI halves their accuracy; PRETA revives after 2 turns, AZHI after 3, at half HP, both full HP after battle; MR. MU's PRETA is Lv25, owned PRETA/AZHI below Lv50 become Lv50 at the ritual; X items / GUARD SPEC / DIRE HIT have no effect on BLACK.

- v50-v54 (redux 4+): PRETA/AZHI traits and revival, GHOST refuses in the TOWER, LAVENDER music as BLACK, MR. MU locations + Mansion AMBER -> AZHI, Tower 7F channelers/door/altar stash, v54 MOM among the channelers after the ritual (picture 33, object 15, D466 bit7 = first talk done; table markers in ch54 are $8A/$8B) (see READMEs). Code for v51+ lives in bank 30 (2F is full). The GB draws at most ten sprites (player included); 15 objects slow the overworld (v53 swaps the long 7F list in only at stage 5 via LoadMapHeader).
