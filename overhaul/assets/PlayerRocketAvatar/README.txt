PlayerRocketAvatar - the player's look after joining TEAM ROCKET (approved design, NOT implemented in the ROM yet)

card_front_56x56.json / .png   Trainer card (RedPicFront replacement), 56x56, 4 Game Boy shades (0 white, 1 light grey, 2 dark grey, 3 black).
                               Made from the user's reference (card_reference_5shade.png, 6x scale): black hat + jacket with dark grey folds,
                               inner shirt dark grey (the reference's 5th shade mapped to dark grey), a white inner edge along both jacket
                               sides next to the shirt (rows <= 32). card_front_x4.png = preview.
map_sprite_6frames.json/.2bpp  Overworld sprite, RED's 6 frames (down, up, left, down walk, up walk, left walk; right = left mirrored),
                               2bpp tiles in RED's sheet order (24 tiles, 384 bytes, same layout as 5:4180). Colour 1 = white, 2 = grey/green
                               (OBP0 light), 3 = black. All clothes black; hat tip + 2 chest pixels grey/green (front); backpack rim grey/green
                               (back / side). make_map_sprite.py rebuilds it from RED's v1 sprite (python make_map_sprite.py OUTDIR).
map_sprite_preview.png / map_sprite_walk.gif  previews.
To implement later: swap the player's map sprite sheet (like BLACK's 2D:7000) and the trainer-card / RedPicFront picture while the player is in TEAM ROCKET.
