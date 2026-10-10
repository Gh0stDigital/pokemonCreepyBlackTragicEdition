Creepy Black Mu v33 (on v32): PRETA's back picture shaded like its front picture.

The front (B:79E8, 48x48) shades the bones with grey gradients hugging the black lines (black -> dark grey -> light
grey -> white, a bit heavier on the lower/right shadow sides; ~10% light, ~9% dark). The back (B:7F3C, 32x32) now does
the same inside the body (preta_back.front_style2 'I'): where a white area is at least 3 px wide, the pixel just
above/left of a black line is dark grey and the next one light grey. Thin white bands between double lines, the
background and the black outline are unchanged; the v32 light-grey rib lines stay. 163 bytes (slot 191).
Previews: qa_ref/v33_preta_back_variants.png (front, v32, D/E/F = too heavy), qa_ref/v33_preta_back_variants2.png
(front, v32, G, H, I = used), qa_ref/v33_preta_back_battle.png (v32 vs v33 in a battle).
Test: t42_v33.py.
