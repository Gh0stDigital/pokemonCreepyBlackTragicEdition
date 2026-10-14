# Creepy Black Mu v56: BRUNO as BLACK (the POKeMON LEAGUE, part 3).
#   - His before-battle and defeat speeches are new when the player is BLACK (D46C); the GHOST route keeps the originals.
#   - His fight is mandatory (he dies in the phase), so nothing is said after the battle: the after-battle text is skipped
#     and the door opens by itself (EndTrainerBattle re-runs the map-load code that opens the exit block).
import json
from patchlib import *
from patchguard import fo
from sm83asm import asm

V55_SHA='e7e6c466720016fff8db0622c11e1d8dc2152206d0823eabe0e3853f77a5da86'
rom=Rom('Creepy_Black_Mu_v55.gb',V55_SHA)
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
T={'t_before':convo(["I am BRUNO of the ELITE FOUR!",
 "Through rigorous training, people and # can become stronger! I've weight trained with my #!",
 "I won't let a monster like you disgrace the sacred bond between trainer and #!",
 "RED! We will grind you down with our superior power! Hoo hah!"]),
 't_defeat':convo(["Why? How could I lose?","My #... Forgive me...","This monster is too powerful..."])}
BANK=0x30;CODE=0x6200
assert not any(R[fo(BANK,CODE):fo(BANK,CODE+0x400)])
TXT=''.join(f"{k}: db {','.join(str(x) for x in v)}\n" for k,v in T.items())
c30,L30=asm(TXT,CODE)
rom.put(fo(BANK,CODE),c30,'Bank 30: v56 BRUNO texts')
# ---- bank 1D: TX_ASM choosers + the end-battle tail
B1D=0x7e6c
assert not any(R[fo(0x1d,B1D):fo(0x1d,0x8000)])
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
c1d,L1d=asm(stub('sb',0x63c3,0)+stub('se',0x63c8,0)+f'''
endtail:
    ld a,[{BLACKF:#x}]
    and a
    ret nz
    ld a,1
    ldh [$8c],a
    jp $294d
''',B1D)
rom.put(fo(0x1d,B1D),c1d,'Bank 1D: v56 BRUNO text choosers (BLACK) + end-battle tail (no after text for BLACK)')
H=fo(0x1d,0x63b0)
assert R[H:H+6].hex()=='c363cd63c863'
rom.data(H,bytes.fromhex(le(L1d['sb'])),"BRUNO's before-battle text -> v56 chooser",'c363')
rom.data(H+4,bytes.fromhex(le(L1d['se'])),"BRUNO's defeat text -> v56 chooser",'c863')
E=fo(0x1d,0x63a1);assert R[E:E+7].hex()=='3e01e08cc34d29'
rom.code(E,bytes.fromhex('c3'+le(L1d['endtail']))+bytes(4),"BRUNO end-battle script: tail -> endtail (no text as BLACK)",R[E:E+7].hex())
rom.finish('Creepy_Black_Mu_v56.gb','manifest_v56.json','CREEPY MU V55',extra=dict(labels=dict(bank1d={k:hex(v) for k,v in L1d.items()},bank30={k:hex(v) for k,v in L30.items()})))
