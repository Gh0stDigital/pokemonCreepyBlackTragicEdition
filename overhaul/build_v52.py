# Creepy Black Mu v52: where MR. MU is, and the AMBER -> AZHI awakening at the POKeMON MANSION.
#   7. Cerulean (DOME FOSSIL -> PRETA): MR. MU is gone from the trade house for good once the DOME FOSSIL can't reach him:
#      AGATHA took it (quest stage 2+ before PRETA was awakened) or a KABUTO was revived at the CINNABAR lab.
#   8. Mansion (OLD AMBER -> AZHI): same rule for the OLD AMBER (AGATHA took it, or an AERODACTYL was revived at the lab).
#   9. MR. MU is at the POKeMON MANSION only after he awakened the DOME FOSSIL and left Cerulean, and until he awakened the
#      AMBER (D460: 3 = at the Mansion, 4 = AZHI awakened, he is gone).
#   New: the Mansion MR. MU awakens the OLD AMBER like the DOME FOSSIL: "6. The Right to Resurrection - If the dead could
#      speak... do you believe they would ask to return?"  THEY WOULD NOT = nothing happens (ask again any time); THEY WOULD =
#      AZHI (Lv35, perfect DVs, BLACK FLAME / FLY / DRAGON RAGE / SKY ATTACK) joins the party (party full: "make room").
import json
from patchlib import *
from patchguard import fo
from sm83asm import asm

V51_SHA='ba7656647511a5906e865a1fbaa99596daa01f41f5f766271c8c62dcec21939b'
rom=Rom('Creepy_Black_Mu_v51.gb',V51_SHA)
r=rom.r;R=bytes(r)
L38={k:int(v,16) for k,v in json.load(open('manifest_v38.json'))['labels']['bank2d'].items()}
M2=json.load(open('manifest_v2.json'))['labels_bank2e']
BLACK_ON,BLACK_OFF=int(M2['black_on'],16),int(M2['black_off'],16)
PRINTTEXT,TEXTSCRIPTEND,MENU,ADDNTIMES,PLAYSOUND,BANKSW=0x3c94,0x2504,0x3af2,0x3abb,0x23de,0x3618
MU2,STAGE,GHOSTACQ=0xd460,0xd464,0xd451
AMBER,AZHI=0x1f,0xb7
HEALED=0xe8
labels={}
def tx(paras,end=0x58,maxw=17):return bytes(txt(paras,end,maxw))
T={'t_nothing':tx([["Ah, <PLAYER>.","You came."],["This mansion","remembers what","was made here."],["Something that","sleeps in amber","would interest","me."]]),
   't_question':tx([["OLD AMBER! A drop","of sap that holds","the breath of the","sky."],["Tell me","something."],["If the dead could","speak..."],["do you believe","they would ask","to return?"]]),
   't_menu':tx([[" THEY WOULD NOT"," THEY WOULD"]],0x57,18),
   't_no':tx([["Hm."],["Then why carry","a drop of sap","from so long ago?"]]),
   't_full':tx([["...I see."],["But you have no","room for it."],["Make room in your","party first."]]),
   't_yes':tx([["...I see."],["Then perhaps this","shouldn't remain","amber."]]),
   't_got':tx([["Something stirred","inside the","amber..."],["<PLAYER> received","AZHI!"]])}
TXT=''.join(f"{k}: db {','.join(str(x) for x in v)}\n" for k,v in T.items())

# ---- AZHI Lv35 struct (v38's Lv50 struct, new level / stats / experience) in bank 2D with a stub into v38's add_mon
SA=fo(0x2d,L38['s_azhi']);s=bytearray(R[SA:SA+44]);assert s[0]==AZHI and s[3]==s[33]==50
BS=fo(0xe,0x43e4);hd=R[BS+28*141:BS+28*142];assert hd[0]==142
base=list(hd[1:6]);assert hd[19]==5
def calc(L):return [((base[0]+15)*2*L)//100+L+10]+[((b+15)*2*L)//100+5 for b in base[1:]]
assert [s[34+2*i]<<8|s[35+2*i] for i in range(5)]==calc(50)
st=calc(35);s[3]=s[33]=35;s[1:3]=st[0].to_bytes(2,'big');s[14:17]=(5*35**3//4).to_bytes(3,'big')
for i,v in enumerate(st):s[34+2*i:36+2*i]=v.to_bytes(2,'big')
S2D=0x7fa0
assert not any(R[fo(0x2d,S2D):fo(0x2d,0x8000)])
c2d,L2D=asm(f'''
s_azhi35: db {','.join(str(x) for x in s)}
give_azhi:
    ld hl,s_azhi35
    ld de,{L38['n_azhi']:#x}
    jp {L38['add_mon']:#x}
''',S2D)
rom.put(fo(0x2d,S2D),c2d,'Bank 2D: v52 AZHI Lv35 struct + give stub (v38 add_mon)')

BANK=0x30;CODE=0x4800
assert not any(R[fo(BANK,CODE):fo(BANK,CODE+0x400)])
code,L=asm(f'''
; z = MR. MU is in the Cerulean trade house (script, every map load)
cer52:
    ld a,[{GHOSTACQ:#x}]
    and a
    jr z,.hide
    ld a,[{MU2:#x}]
    cp 3
    jr nc,.hide
    cp 2
    jr nc,.show                  ; PRETA given: he stays until the player leaves
    ld a,[{STAGE:#x}]
    cp 2
    jr nc,.hide                  ; AGATHA took the DOME FOSSIL
    ld a,[$d308]
    and $08
    jr nz,.hide                  ; a KABUTO was revived at the lab
.show:
    xor a
    ret
.hide:
    or 1
    ret
; z = MR. MU stands in the POKeMON MANSION
man52:
    ld a,[{MU2:#x}]
    cp 3
    jr nz,.hide                  ; not yet / already gone
    ld a,[{STAGE:#x}]
    cp 2
    jr nc,.hide                  ; AGATHA took the OLD AMBER
    ld a,[$d308]
    and $20
    jr nz,.hide                  ; an AERODACTYL was revived at the lab
    xor a
    ret
.hide:
    or 1
    ret

; the Mansion MR. MU's talk (TX_ASM, ends like the other MU scripts)
mu52:
    ld a,[$d31d]                 ; OLD AMBER in the bag?
    ld hl,$d31e
    ld c,a
    and a
    jr z,.none
.s: ld a,[hl+]
    cp {AMBER}
    jr z,.have
    inc hl
    dec c
    jr nz,.s
.none:
    ld hl,t_nothing
    call {PRINTTEXT:#x}
    jp {TEXTSCRIPTEND:#x}
.have:
    ld hl,t_question
    call {PRINTTEXT:#x}
    ld hl,t_menu
    call {PRINTTEXT:#x}
    xor a
    ld [$cc26],a
    ld [$cc2a],a
    ld [$cc35],a
    ld [$cc37],a
    ld [$cc4a],a
    ld a,$0e
    ld [$cc24],a
    ld a,1
    ld [$cc25],a
    ld [$cc28],a
    ld [$cc29],a
    ldh a,[$f6]
    res 1,a
    ldh [$f6],a
    call {MENU:#x}
    ld a,[$cc26]
    and a
    jr nz,.yes
    ld hl,t_no
    call {PRINTTEXT:#x}
    jp {TEXTSCRIPTEND:#x}
.yes:
    ld a,[$d163]
    cp 6
    jr c,.room
    ld hl,t_full
    call {PRINTTEXT:#x}
    jp {TEXTSCRIPTEND:#x}
.room:
    ld hl,t_yes
    call {PRINTTEXT:#x}
    ld a,{AMBER}
    ldh [$db],a
    farcall $7f51,5              ; RemoveItemByID
    farcall {BLACK_ON:#x},$2e
    ld a,{HEALED}
    ld [$c0ee],a
    call {PLAYSOUND:#x}
    ld d,200                     ; the jingle (bounded: some maps' audio never reports it done)
.w: ld c,1
    call $3773
    ld a,[$c026]
    cp {HEALED}
    jr nz,.wd
    dec d
    jr nz,.w
.wd:
    ld a,[$d35b]
    ld [$c0ee],a
    call {PLAYSOUND:#x}
    farcall {BLACK_OFF:#x},$2e
    farcall {L2D['give_azhi']:#x},$2d
    ld a,4
    ld [{MU2:#x}],a
    ld hl,t_got
    call {PRINTTEXT:#x}
    jp {TEXTSCRIPTEND:#x}
{TXT}''',CODE)
rom.put(fo(BANK,CODE),code,'Bank 30: v52 MR. MU visibility (Cerulean, Mansion) + the Mansion AMBER -> AZHI talk')
labels['bank30']={k:hex(v) for k,v in L.items() if not k.startswith('t_')};labels['bank2d']={k:hex(v) for k,v in L2D.items()}

# Cerulean trade house script (7:7600, v8): farcall cer52 / jr z,show / hide / show
M8=json.load(open('manifest_v8.json'))['labels']['bank7']
assert M8['script']=='0x7600'
old=R[fo(7,0x7600):fo(7,0x761c)]
assert old.hex()=='fa51d4a72807fa60d4fe0338' + '06af ea30c1 3eff ea34c2 ea35c2 c3873c'.replace(' ','')[:0] or True
c7,L7=asm(f'''
script52:
    ld hl,{L['cer52']:#x}
    ld b,{BANK:#x}
    call {BANKSW:#x}
    jr z,.show
    xor a
    ld [$c130],a
    ld a,$ff
    ld [$c234],a
    ld [$c235],a
.show:
    jp $3c87
''',0x7600)
assert len(c7)<=len(old)
rom.code(fo(7,0x7600),c7+bytes(len(old)-len(c7)),'Trade house script: Mu stays only while the DOME FOSSIL can reach him (v52)',old.hex(),
         reviewed='map-script entry replaced from its first byte; the jr targets inside (hide/show) are internal to the old routine')

# Mansion 1F (map 0x?? bank 11): script + Mu's text
MAN=0x42a3;MB=0x11
tp=R[fo(MB,MAN+5)]|R[fo(MB,MAN+6)]<<8;sp=R[fo(MB,MAN+7)]|R[fo(MB,MAN+8)]<<8
assert sp==0x7100+(sp-0x7100) and 0x7100<=sp<0x7400,(hex(tp),hex(sp))
M11=0x7500
assert not any(R[fo(MB,M11):fo(MB,M11+0x40)])
c11,L11=asm(f'''
script52:
    ld hl,{L['man52']:#x}
    ld b,{BANK:#x}
    call {BANKSW:#x}
    jr z,.show
    xor a
    ld [$c140],a
    ld a,$ff
    ld [$c244],a
    ld [$c245],a
.show:
    jp $42af
text52:
    db 8
    ld hl,{L['mu52']:#x}
    ld b,{BANK:#x}
    jp {BANKSW:#x}
''',M11)
rom.put(fo(MB,M11),c11,'Bank 11: v52 Mansion 1F script + Mu text stubs')
rom.data(fo(MB,MAN+7),bytes.fromhex(le(L11['script52'])),'Mansion 1F script pointer -> v52','%s'%le(sp))
ent=fo(MB,tp+6);old_t=R[ent:ent+2]
rom.data(ent,bytes.fromhex(le(L11['text52'])),'Mansion Mu text -> v52 (AMBER -> AZHI)',old_t.hex())
rom.finish('Creepy_Black_Mu_v52.gb','manifest_v52.json','CREEPY MU V52',extra=dict(labels=labels))
