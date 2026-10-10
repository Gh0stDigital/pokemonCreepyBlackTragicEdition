# Creepy Black Mu v32: GHOST can't eat PRETA or AZHI; PRETA's back picture gets light-grey rib shading.
#   1. Hunger victim (v30) skips PRETA (B6) and AZHI (B7): the nearest Pokemon in front of GHOST it can eat, else the
#      nearest below it (GHOST leading: just below), else the player. Without GHOST in the party: the last edible one.
#      The 50-step warning names the same victim. (victim2 at 2D; the v30 routine now jumps there.)
#   2. PRETA (fossil KABUTOPS) back picture: the rib lines v8 had made white are light grey (colour 1); black outline,
#      white body otherwise unchanged (preta_back.py variant A).
# Logged patches on top of verified Mu v31 (patchlib).
import io,json,sys
from patchlib import *
from patchguard import fo
from sm83asm import asm
sys.path.insert(0,str(ROOT.parent/'ref'));import pic
import preta_back as P

V31_SHA='d093575eb53df4fc79dc98481f8d0c193d8746ff947346ce08fe169b00ae2fa1'
rom=Rom('Creepy_Black_Mu_v31.gb',V31_SHA)
r=rom.r;R=bytes(r)
GHOST,PRETA,AZHI=0x1f,0xb6,0xb7
BANK=0x2d
VICTIM=int(json.load(open('manifest_v30.json'))['labels']['bank2d']['victim'],16)
L31=json.load(open('manifest_v31.json'))['labels']['bank2d']
CODE=0x6080
assert CODE>max(int(v,16) for v in L31.values())+0x40

# ---- 1. victim2
code,L=asm(f'''
victim2:                          ; a = party index GHOST will eat, $FF = the player. PRETA / AZHI are never eaten.
    ld a,[$d163]
    ld b,a
    ld hl,$d164
    ld c,0
.f: ld a,c
    cp b
    jr nc,.noghost
    ld a,[hl+]
    cp {GHOST}
    jr z,.g
    inc c
    jr .f
.g: ld e,c                        ; in front of GHOST first (nearest first)
.up:ld a,e
    and a
    jr z,.dn
    dec e
    ld a,e
    call edible
    jr z,.up
    ld a,e
    ret
.dn:ld e,c                        ; then below it
.d2:inc e
    ld a,e
    cp b
    jr nc,.player
    call edible
    jr z,.d2
    ld a,e
    ret
.noghost:                         ; GHOST not in the party: the last edible one
    ld e,b
.n2:ld a,e
    and a
    jr z,.player
    dec e
    ld a,e
    call edible
    jr z,.n2
    ld a,e
    ret
.player:
    ld a,$ff
    ret
edible:                           ; a = party index -> Z = can't be eaten (GHOST, PRETA, AZHI)
    ld hl,$d164
    add l
    ld l,a
    jr nc,.n
    inc h
.n: ld a,[hl]
    cp {GHOST}
    ret z
    cp {PRETA}
    ret z
    cp {AZHI}
    ret
''',CODE)
assert CODE+len(code)<0x6400
rom.put(fo(BANK,CODE),code,'Bank 2D: v32 hunger victim (never PRETA / AZHI)')
rom.code(fo(BANK,VICTIM),bytes.fromhex('c3'+le(L['victim2'])),'v30 victim -> victim2 (PRETA/AZHI immune)',R[fo(BANK,VICTIM):fo(BANK,VICTIM)+3].hex(),
         reviewed='the only jumps into the old routine are its own internal jr targets after these 3 bytes')

# ---- 2. PRETA back picture
BACK=fo(*P.BACK);SLOT=191
cur=P.load(str(ROOT/'Creepy_Black_Mu_v31.gb'));v6=P.load(str(ROOT/'Creepy_Black_Mu_v6.gb'));v7=P.load(str(ROOT/'Creepy_Black_Mu_v7.gb'))
new=P.variant(cur,v6,v7,'A');d=P.raw(new)
packed=bytes(pic.compress(d));assert bytes(pic.decompress(io.BytesIO(packed)))==d and packed[0]==R[BACK]
grey=sum(1 for row in new for c in row if c==1)
if len(packed)<=SLOT:
    rom.data(BACK,packed.ljust(SLOT,b'\0'),'PRETA back picture: light-grey rib shading (%d px, %d bytes)'%(grey,len(packed)),R[BACK:BACK+SLOT])
else:
    raise SystemExit('back picture %d bytes > slot %d'%(len(packed),SLOT))
rom.finish('Creepy_Black_Mu_v32.gb','manifest_v32.json','CREEPY MU V32',extra=dict(labels=dict(bank2d={k:hex(v) for k,v in L.items()}),preta_back=dict(grey_px=grey,bytes=len(packed))))
