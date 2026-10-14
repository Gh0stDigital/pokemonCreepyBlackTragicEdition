Creepy Black Mu v54 (from v53): the player's "mother" among the channelers on Tower 7F
SHA-256 2990501f89adfb111240a51ba6211731bca973bfec3598bfd130a1777e3f07a2

- After the ritual (D467 = 6, the player is BLACK) the channelers stay in the 7F hall and the player's MOM sprite (picture 33) stands
  among them, left column, row 9 (object 15, text id 20). The long list (15 objects) is loaded at stage 5 whatever the ritual state.
- First talk: the confession ("Oh! Hello, honey!" ... "And I'll always be here to support you, just as I always have!"); sets D466 bit7.
  Later talks: the short one ("Oh? What's that, honey?" ... "You've really become a man now! Hehe!").
- Slots after the ritual (AGATHA is object 9 again): channelers 10-14, 5, 4, 6, 7, 8; MOM = 15. Before the ritual: as v53 (no MOM; object 15 is
  a channeler). Same distance rule as v53 (only people within two rows of the player are drawn).
- Code: bank 30:5800 ch54 (replaces ch53 in tail53), objsel54 (LoadMapHeader), mom54; bank 18:70A3 object list + text table (20 entries).
  script53 .post no longer shrinks numsprites to 9. Slot markers in ch54's tables are $8A/$8B (a plain 10/11 is a channeler slot).
- Tests: t62_v54.py mom. t53_v45.py tower fights with the map id set elsewhere (GHOST refuses in the Tower since v51).
Static: check_hooks.py 138 hooks, 0 problems.
