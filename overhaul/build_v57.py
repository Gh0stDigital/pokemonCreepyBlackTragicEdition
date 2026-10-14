# Creepy Black Mu v57: LANCE as BLACK (the POKeMON LEAGUE, part 4).
#   - His before-battle and defeat speeches are new when the player is BLACK (D46C); the GHOST route keeps the originals.
#   - His fight is mandatory (he dies in the phase), so nothing is said after the battle: the after-battle text is skipped
#     and the door opens by itself (EndTrainerBattle re-runs the map-load code that opens the exit block).
import json
from patchlib import *
from patchguard import fo
from sm83asm import asm

V56_SHA='849cf31ebf896ffde644cacb77697f0364e8e71612cd9b508fe1951241861d42'
rom=Rom('Creepy_Black_Mu_v56.gb',V56_SHA)
r=rom.r;R=bytes(r)
PRINTTEXT,TEXTEND=0x3c94,0x2504
BLACKF=0xd46c
def wrap(s,w=17):
    out=[];cur=''
    for word in s.split():
        if cur and shown(cur+' '+word)>w:out.append(cur);cur=word
        else:cur=(cur+' '+word) if cur else word
    out.append(cur);return out
def convo(parts):return bytes(txt([wrap(p) for p in parts],0x58,17))
T={'t_before':convo(["So... The others have fallen. Then it must be true.",
 "I am LANCE, leader of the ELITE FOUR!",
 "The blood of the BUSHI runs through my veins! On my honor as a dragon trainer, I swear to destroy you, BLACK!",
 "For my comrades, and the countless lives you've taken in KANTO!",
 "Your reign of terror ends here!"]),
 't_defeat':convo(["Impossible... This power...","Could it be the one spoken of in my ancestors' legends?","No... This cannot be how it ends!"])}
BANK=0x30;CODE=0x6400
assert not any(R[fo(BANK,CODE):fo(BANK,CODE+0x400)])
TXT=''.join(f"{k}: db {','.join(str(x) for x in v)}\n" for k,v in T.items())
c30,L30=asm(TXT,CODE)
rom.put(fo(BANK,CODE),c30,'Bank 30: v57 LANCE texts')
# ---- bank 1D: TX_ASM choosers + the end-battle tail
B1D=0x7000
assert not any(R[fo(0x16,B1D):fo(0x16,0x8000)])
def stub(name,old,new):
    return f'''
{name}: db 8
    ld a,[{BLACKF:#x}]
    and a
    ld hl,{old:#x}
    jr z,.p
    ld hl,far_{name}
.p: call {PRINTTEXT:#x}
    jp {TEXTEND:#x}
far_{name}: db $17,{L30[("t_before" if name=="sb" else "t_defeat")]&255},{L30[("t_before" if name=="sb" else "t_defeat")]>>8},{BANK},$50
'''
c1d,L1d=asm(stub('sb',0x63ae,0)+stub('se',0x63b3,0)+f'''
endtail:
    ld a,[{BLACKF:#x}]
    and a
    jr z,.orig
    ld hl,$d866                  ; the after text would have set the 'beat LANCE' flag
    set 6,[hl]
    ret
.orig:
    ld a,1
    ldh [$8c],a
    jp $294d
''',B1D)
rom.put(fo(0x16,B1D),c1d,'Bank 1D: v57 LANCE text choosers (BLACK) + end-battle tail (no after text for BLACK)')
H=fo(0x16,0x639b)
assert R[H:H+6].hex()=='ae63b863b363'
rom.data(H,bytes.fromhex(le(L1d['sb'])),"LANCE's before-battle text -> v57 chooser",'ae63')
rom.data(H+4,bytes.fromhex(le(L1d['se'])),"LANCE's defeat text -> v57 chooser",'b363')
E=fo(0x16,0x6354);assert R[E:E+7].hex()=='3e01e08cc34d29'
rom.code(E,bytes.fromhex('c3'+le(L1d['endtail']))+bytes(4),"LANCE end-battle script: tail -> endtail (no text as BLACK)",R[E:E+7].hex())
rom.finish('Creepy_Black_Mu_v57.gb','manifest_v57.json','CREEPY MU V55',extra=dict(labels=dict(bank16={k:hex(v) for k,v in L1d.items()},bank30={k:hex(v) for k,v in L30.items()})))
