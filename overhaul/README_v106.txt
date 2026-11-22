Creepy Black Mu v106 (on v105): TEAM ROCKET route, part 1 - the contract on BROCK
SHA-256: f03c5a36d760bdf8413e2724b0c45e8cd4f42df5a064052059a4ae6286346cfc

The ROCKET route opens once GHOST has killed at least one trainer (GHOST route, never as BLACK).
- PEWTER MUSEUM 1F: a ROCKET stands above the top fossil exhibit (y1 x3, facing it) as soon as any trainer kill bit is set
  (D4A4-D4AD, D430-D44F, D886). First talk: annoyed ("What're you staring at, kid?"), then he takes a good look: "eyes of a killer",
  jokes that you might be the brat everyone whispers about who kills POKeMON and people, and offers a real target: his constituents
  want the PEWTER GYM leader eliminated, he'll pay well, doesn't care how, no witnesses, he can't help you if you get caught.
- Until BROCK is dead he only reminds you ("BROCK is still breathing, kid.").
- BROCK dead (kill index 12 = D4A5 bit 4): "I heard the news... Clean work, kid", the player receives 10000 (item jingle),
  then "I like you, kid... what it takes to join TEAM ROCKET... Go to CERULEAN CITY and take the test" (the test is the next part).
  After that he repeats "take the test"; once the player leaves the museum he is gone.
- BROCK already dead when they first meet: no contract, "BROCK is already dead... That was you, wasn't it?" and he pays at once.
- Witnesses: if BROCK dies under contract while his gym trainer (kill index 13 = D4A5 bit 5) is still alive, NOTORIETY +5 (v71: the
  Saffron gate guards' fees). Killing the trainer first, or killing BROCK without a contract, adds nothing.

Data: D84A (unused event-flag byte) = quest state (low nibble 0 not met / 1 contract / 2 paid / 3 gone; bit 6 witness checked).
Code: bank 32:5800 (vis106 museum visibility, rk106 talk, wit106 witness check; texts 32:5A00), bank 17:6000 (museum 1F object data copy
+ ROCKET as object 6, text table copy + entry 6, talk stub, museum and PEWTER GYM map-script wrappers), 2E:7FC0 ml106 = first link of
the 2E:4000 map-load chain (state 2 -> 3). Museum 1F has no signs, so the new object's text id hijacks nothing.

Test: t107_v106.py vis / flow / already / witness / npcs (the museum's other people unchanged, compared with v105); t98_v90.py
kill / spare / win (BROCK) still pass. Note: the test states in qa/ were rebuilt this version (new container): t1 .. t5 chain.
