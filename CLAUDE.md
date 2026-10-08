# Pokémon Creepy Black — Tragic Edition (Mu overhaul)

Binary ROM hack of the 1 MiB Game Boy ROM "Pokémon Black (Creepy)". Every version is built by a
Python script that applies **logged patches with old-byte asserts** on top of the previous verified ROM.
Never overwrite an earlier ROM; build a new version (v6, v7, …) and keep ROM length exactly 1,048,576 bytes.

## Layout
- `Creepy_Black_Mu_v1.gb` … `v13.gb` (root and `overhaul/`): builds. Latest = **v13**
  (SHA-256 2fa351de1eca04f63f96abe47469287eccfc3754f6437c0411d5f81ecf7098a4).
- `edit/`: original v1 handoff (v1 build.py, which needs the clean base ROM that is NOT in this repo).
- `overhaul/build_v2.py … build_v13.py`: each takes the previous version, checks its SHA, writes the next
  ROM + `manifest_vN.json` (before/after bytes per patch). READMEs: `README_v2.txt`, `README_v3.txt`, `README_v6.txt`, `README_v7.txt`, `README_v8.txt`, `README_v9.txt`, `README_v10.txt`, `README_v11.txt`, `README_v12.txt`, `README_v13.txt`.
- `overhaul/harness.py` + `t*.py`: PyBoy emulator tests. `run_all.sh` (v2 features), `run_v3.sh` (full chain
  including the Mirage tests), `run_v6.sh` (Cerulean Mu / PRETA / MACABRE; needs the chain's
  `pallet_with_ghost` state), `run_v7.sh` (v6 checks + PRETA revival / Silph Scope effect), `run_v8.sh`
  (v7 checks + Mansion Mu / PRETA in Mirage battles), `run_v9.sh` (v8 checks + PRETA vs PRETA,
  Rare Candy, Pokémon Center), `run_v10.sh` (v9 checks + AZHI / BLACK FLAME / ?????), `run_v11.sh` (same suite on v11), `run_v12.sh` (v10 suite + rival BLUE, t25_blue.py), `run_v13.sh` (v12 suite + Pokémon Center/Mart, t26_center.py). Tests chain through save states in `overhaul/qa/` (gitignored; the chain
  regenerates them starting at `t1_opening.py`). Select the ROM with `CB_ROM=Creepy_Black_Mu_v5.gb`.
- Patch safety (static, no emulator): `overhaul/patchguard.py` (SM83 decoder + checks), `overhaul/patchlib.py`
  (shared build helpers: `Rom.put/data/code/hook/finish`), `overhaul/check_hooks.py` (re-checks all 42 hooks v1-v13
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

## Making a new version (v14+)
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
- The base game's trainer-kill step is a second "battle" (wBattleType 3) after winning with CURSE; scripted
  trainers (no trainer header) normally get "But, it failed!" there (check at F:5033).

## Saved RAM used by the overhaul (D450–D4AD cleared on NEW GAME)
All of it is inside the saved block (wMainData D2F7–DA80); `t27_saveload.py` proves save → power cycle → CONTINUE
keeps D450–D463 and the gravestones, and NEW GAME over an old save clears them. New flags must stay in D450–D4A3.
D450 Mu answer (1 Trainer, 2 Pokémon) · D451 Ghost acquired · D452 Curse used this battle · D453 trainer
killed by Curse · D454 Mu state · D455 Ghost hunger · D456 hunger step counter · D457–D45A temp ·
D45B police alert shown this map · D45C Ghost-use counter · D45D Mirage battle active · D45E alive mask ·
D45F Ghost deposited for Mirage · D460 Mu state after Mt. Moon (0/1 introduced/2 PRETA given/3 moved to Mansion 1F) · D461 PRETA revival countdown · D462 temp: Pokémon Center heal running · D463 rival mode (0 normal/1 shock/2 hero). Do not use D485–D4A3 (real game data) or D4A4–D4AF (gravestones etc.).

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
during the nurse's heal, fixed v12 trainer-curse register clobber (scripted trainers unkillable again).
