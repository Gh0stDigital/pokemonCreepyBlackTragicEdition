# Creepy Black Mu v33: PRETA's back picture shaded like its front picture.
#   The front (B:79E8, 48x48) draws its bones with grey gradients hugging the black lines (black -> dark grey -> light
#   grey -> white, a bit heavier on the lower/right shadow sides). The back (32x32) now does the same inside the body
#   (preta_back.front_style2 'I' on the v32 picture): where a white area is at least 3 px wide, the pixel right above /
#   left of a black line is dark grey and the next one light grey; thin white bands between double lines stay white,
#   the light-grey rib lines stay. Variants: qa_ref/v33_preta_back_variants2.png (G, H, I = used).
import io,sys
from patchlib import *
from patchguard import fo
sys.path.insert(0,str(ROOT.parent/'ref'));import pic
import preta_back as P

V32_SHA='d7270336c2a71c45161a0432fe11ca1fffc8d23633e6584abb55fae051a6dc98'
rom=Rom('Creepy_Black_Mu_v32.gb',V32_SHA)
r=rom.r;R=bytes(r)
BACK=fo(*P.BACK);SLOT=191
cur=P.load(str(ROOT/'Creepy_Black_Mu_v32.gb'))
new=P.front_style2(cur,'I');d=P.raw(new)
packed=bytes(pic.compress(d));assert bytes(pic.decompress(io.BytesIO(packed)))==d and packed[0]==R[BACK]
print('packed',len(packed),'slot',SLOT)
if len(packed)<=SLOT:
    rom.data(BACK,packed.ljust(SLOT,b'\0'),'PRETA back picture: front-style grey gradients (%d bytes)'%len(packed),R[BACK:BACK+SLOT])
else:
    raise SystemExit('too big')
rom.finish('Creepy_Black_Mu_v33.gb','manifest_v33.json','CREEPY MU V33',extra=dict(preta_back=dict(bytes=len(packed))))
