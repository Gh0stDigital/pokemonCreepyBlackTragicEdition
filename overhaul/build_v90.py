# Creepy Black Mu v90: BROCK's after-battle dialogue matches what happened to him (PEWTER GYM, map 36, bank 17).
#   - killed (CURSE in the trainer phase): "<PLAYER> took the BOULDERBADGE from BROCK's body." (new text id 7, like the other leaders' v14 line) and TM34 goes into the bag silently
#     (the base game's kill gave the badge only, with no text at all).
#   - survived, but CURSE was used in the battle (D452): the cheerful "Wait! Take this with you!" / TM34 lecture is replaced by a shaken BROCK ("...Please. Take this and go.",
#     "It's BIDE... Now go. Please. Take that thing away from me!").
#   - survived, no CURSE: the original lines.
#   killchk89 (17:7D80) replaces the "was he killed?" far call at 17:43DF; the text table is copied (7DC0) with ids 4 / 5 = choosers and id 7 = the killed line; header +5 points to it.
from patchlib import *
from patchguard import fo
from sm83asm import asm

V89_SHA='c65fefc4232baeec861e26d91fef50cfcd59b713cce9aa1e320a8f32b14e6def'
rom=Rom('Creepy_Black_Mu_v89.gb',V89_SHA)
R=bytes(rom.r)
def lh(a):return a.to_bytes(2,'little').hex()
A=0x7d80
assert not any(R[fo(0x17,A):fo(0x17,0x8000)])
took=txt([['<PLAYER> took the','BOULDERBADGE from',"BROCK's body."]],end=0x57)
shaken4=txt([['...Please. Take','this and go.']])
advs=txt([["...You're the one",'everyone fears.'],['Go to CERULEAN','GYM. Please.']])
shaken5=txt([["It's BIDE..."],['Now go. Please.','Take that thing','away from me!']])
hh=fo(0x17,int.from_bytes(R[0x1ae+2*0x36:0x1ae+2*0x36+2],'little'))
tp=R[hh+5]|R[hh+6]<<8;assert tp==0x443f,hex(tp)
orig=[R[fo(0x17,tp)+2*i]|R[fo(0x17,tp)+2*i+1]<<8 for i in range(6)]
assert orig[3]==0x44bd and orig[4]==0x44c2
c,L=asm(f'''
killchk89:                       ; (17:43DF) the replaced  ld b,3 / ld hl,4DAC / call 3618  (z = BROCK lives, nz = he was killed); a killed BROCK: the line + TM34
    ld b,3
    ld hl,$4dac
    call $3618
    ret z
    ld a,7
    ldh [$8c],a
    call $294d
    ld bc,$ea01
    call $3e82
    or 1
    ret
adv89:                           ; (17:446C) his later talks: the old advice, unless CURSE was used just now (D452) or the player is a murderer (D453)
    ld hl,$44b8
    ld a,[$d452]
    ld b,a
    ld a,[$d453]
    or b
    jr z,.p
    ld hl,adv_s89
.p: jp $3c94
t4_89: db 8
    ld hl,$44bd
    ld a,[$d452]
    and a
    jr z,.p
    ld hl,s4_89
.p: call $3c94
    jp $2504
t5_89: db 8
    ld a,[$d452]
    and a
    jr nz,.s
    ld hl,$44c2
    call $3c94
    jp $2504
.s: ld hl,recv_89
    call $3c94
    ld hl,s5_89
    call $3c94
    jp $2504
recv_89: db $17,$ad,$40,$26,$0b,$50
s4_89: db {','.join(str(x) for x in shaken4)}
s5_89: db {','.join(str(x) for x in shaken5)}
took_89: db {','.join(str(x) for x in took)}
adv_s89: db {','.join(str(x) for x in advs)}
tab_89: dw {orig[0]:#x},{orig[1]:#x},{orig[2]:#x},t4_89,t5_89,{orig[5]:#x},took_89
''',A,{})
assert A+len(c)<=0x8000
rom.put(fo(0x17,A),c,'Bank 17: v90 BROCK killchk89 / text choosers / killed text / table')
o=fo(0x17,0x43df);assert R[o:o+10].hex()=='06032 1ac4dcd18362024'.replace(' ','')
rom.code(o,bytes([0xcd])+bytes.fromhex(lh(L['killchk89']))+bytes([0x20,0x29])+bytes(5),'BROCK post-battle: killed check -> killchk89 (+ the killed line / TM34)','0603 21ac4d cd1836 2024'.replace(' ',''),
         reviewed='the stub repeats the far call; the jr nz keeps its target (17:440D)')
o=fo(0x17,0x446c);assert R[o:o+6].hex()=='21b844cd943c'
rom.code(o,bytes([0xcd])+bytes.fromhex(lh(L['adv89']))+bytes(3),'BROCK talk after the fight: ld hl,44B8 / call PrintText -> adv89 (shaken advice for a CURSE user / murderer)','21b844cd943c',
         reviewed='adv89 chooses hl and tail-jumps to PrintText (3C94), returning to the caller')
rom.data(hh+5,bytes.fromhex(lh(L['tab_89'])),'PEWTER GYM text table -> v90 copy (4 / 5 choosers, 7 = killed)',lh(tp))
rom.finish('Creepy_Black_Mu_v90.gb','manifest_v90.json','CREEPY MU V90',extra=dict(labels=dict(bank17={k:hex(v) for k,v in L.items()})))
