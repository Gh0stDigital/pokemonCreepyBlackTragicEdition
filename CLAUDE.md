# Pokémon Creepy Black — Tragic Edition (Mu overhaul)

Binary ROM hack of the 1 MiB Game Boy ROM "Pokémon Black (Creepy)". Every version is built by a
Python script that applies **logged patches with old-byte asserts** on top of the previous verified ROM.
Never overwrite an earlier ROM; build a new version (v6, v7, …) and keep ROM length exactly 1,048,576 bytes.

## Layout
- `Creepy_Black_Mu_v1.gb` … `v11.gb` (root and `overhaul/`): builds. Latest = **v11**
  (SHA-256 7fa2b19d9a7584dad94263fba733d5b2a64b4302e71f2c984b36ec2b76271b9f).
- `edit/`: original v1 handoff (v1 build.py, which needs the clean base ROM that is NOT in this repo).
- `overhaul/build_v2.py … build_v11.py`: each takes the previous version, checks its SHA, writes the next
  ROM + `manifest_vN.json` (before/after bytes per patch). READMEs: `README_v2.txt`, `README_v3.txt`, `README_v6.txt`, `README_v7.txt`, `README_v8.txt`, `README_v9.txt`, `README_v10.txt`, `README_v11.txt`.
- `overhaul/harness.py` + `t*.py`: PyBoy emulator tests. `run_all.sh` (v2 features), `run_v3.sh` (full chain
  including the Mirage tests), `run_v6.sh` (Cerulean Mu / PRETA / MACABRE; needs the chain's
  `pallet_with_ghost` state), `run_v7.sh` (v6 checks + PRETA revival / Silph Scope effect), `run_v8.sh`
  (v7 checks + Mansion Mu / PRETA in Mirage battles), `run_v9.sh` (v8 checks + PRETA vs PRETA,
  Rare Candy, Pokémon Center), `run_v10.sh` (v9 checks + AZHI / BLACK FLAME / ?????), `run_v11.sh` (same suite on v11). Tests chain through save states in `overhaul/qa/` (gitignored; the chain
  regenerates them starting at `t1_opening.py`). Select the ROM with `CB_ROM=Creepy_Black_Mu_v5.gb`.
- `ref/`: reverse-engineering helpers. `red.gb` = vanilla Pokémon Red (US) for signature matching;
  `pokered.sym` = pret pokered symbols; `sig.py` locates vanilla routines in this ROM by masked byte
  signatures; `dis.py` = tiny disassembler (`python ref/dis.py ROM BANK ADDR N`); `pic.py` = Gen-1 pic
  (de)compressor.
- `pokeblack/charmap.asm`: pret pokered charmap (used by build text encoding and tests).

## Setup
`pip install pyboy pillow pypng`, then run from `overhaul/` with `PY=python bash run_v3.sh`
(scripts default to a Windows venv path; set `PY`). Set `PYTHONIOENCODING=utf-8`.

## Rules learned the hard way
- Verify bank, CPU address and file offset before patching; pokered addresses are shifted in this ROM.
- Text lines ≤ 17 rendered chars (`#` renders as "POKé", 4 chars): the ▼ arrow eats column 18.
- Outdoor maps can only show sprites in their sprite set (Pallet = set 1 at 0x17AB9).
- Don't claim behavior works until a PyBoy test shows it.
- PyBoy hangs if a test keeps pressing A through the Pokémon Center nurse's goodbye (also on v1); stop at
  "fighting fit".

## Saved RAM used by the overhaul (D450–D4AD cleared on NEW GAME)
D450 Mu answer (1 Trainer, 2 Pokémon) · D451 Ghost acquired · D452 Curse used this battle · D453 trainer
killed by Curse · D454 Mu state · D455 Ghost hunger · D456 hunger step counter · D457–D45A temp ·
D45B police alert shown this map · D45C Ghost-use counter · D45D Mirage battle active · D45E alive mask ·
D45F Ghost deposited for Mirage · D460 Mu state after Mt. Moon (0/1 introduced/2 PRETA given/3 moved to Mansion 1F) · D461 PRETA revival countdown · D462 temp: Pokémon Center heal running. Do not use D485–D4A3 (real game data) or D4A4–D4AF (gravestones etc.).

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
knows DRAGON RAGE (DRAGONBREATH removed), BLACK FLAME faints only Pokémon (spares GHOST/PRETA/AZHI, never harms people).
