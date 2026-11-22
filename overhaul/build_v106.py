# Creepy Black Mu v106 (on v105): TEAM ROCKET route, part 1 - the contract on BROCK.
#  - PEWTER MUSEUM 1F (map 34, bank 17): a ROCKET (picture $18) stands above the top fossil exhibit (y1 x3, facing down) once GHOST has killed
#    at least one trainer (any kill bit in D4A4-D4AD, D430-D44F, D886), on the GHOST route (D451), never as BLACK (D46C).
#    Object 6 is appended to a copy of the map's object data (17:6000); its text id 6 is a new entry of a copied text table (TX_ASM -> rk106).
#    vis106 (map script wrapper) hides him (picture 0, position FF) when he should not be there. Museum 1F has no signs: no text id is hijacked.
#  - Quest state D84A (an event-flag byte no code or trainer header uses): low nibble 0 not met, 1 contract given, 2 paid, 3 gone (the map-load
#    chain moves 2 -> 3, so he leaves once the player has left the museum); bit 6 = the witness check ran.
#  - Talk: annoyed, then "eyes of a killer", the joke about the rumoured killer, the contract on the PEWTER GYM leader (pay well, any way, no
#    witnesses, he can't help if you get caught). BROCK dead (kill index 12 = D4A5 bit 4): his news, Y10000 (BCD +1 on D347, capped at 999999)
#    with the item jingle, "I like you ... TEAM ROCKET ... take the test in CERULEAN" (the test is the next part). If BROCK was already dead when
#    they first meet, the contract is skipped and he pays at once.
#  - Witnesses: PEWTER GYM's map script runs wit106: when BROCK has died under contract (state 1) and his gym trainer (kill index 13 = D4A5 bit 5)
#    is still alive, NOTORIETY (D85C, v71: Saffron gate fees) +5 (once).
from patchlib import *
from patchguard import fo
from sm83asm import asm
V105_SHA='c2b9598be23c3122f6ea1cd53e4942756e6db3ee2fe8125d0d8a4b98b67d7f4c'
rom=Rom('Creepy_Black_Mu_v105.gb',V105_SHA)
R=bytes(rom.r)
B17=0x17;B32=0x32;MUS=0x34;GYM=0x36
STATE=0xd84a;NOTOR=0xd85c;ROCKET=0x18
PRINTTEXT,TEXTEND,BANKSW=0x3c94,0x2504,0x3618
def wrap(s,w=17):
    out=[];cur=''
    for word in s.split():
        if cur and len(cur.replace('#','POKe'))+1+len(word.replace('#','POKe'))>w:out.append(cur);cur=word
        else:cur=(cur+' '+word) if cur else word
    out.append(cur);return out
def speech(*ss,end=0x58):return bytes(txt([wrap(s) for s in ss],end,17))
T={
 'intro':speech("ROCKET: Hey! What're you staring at, kid?","Get lost before I...","...","Hold on.","Let me get a good look at you.",
                "Heh... Those eyes.","You've got the eyes of a killer, kid.",
                "Say... You wouldn't be that brat everyone's whispering about?",
                "The one going around killing #MON... and people?","Hahaha! Just kidding.","...Unless I'm not."),
 'contract':speech("Listen. How about taking down a real target?",
                   "My constituents would like to see the PEWTER GYM leader eliminated.","Do it and I'll pay you well.",
                   "I don't care how you do it.","Just don't leave any witnesses.","If you get caught, I can't help you."),
 'already':speech("...Wait.","The PEWTER GYM leader... BROCK is already dead.","That was you, wasn't it? Heh.",
                  "My constituents wanted him gone.","Looks like you did the job before I even asked."),
 'remind':speech("ROCKET: BROCK is still breathing, kid.","Come back when the job is done.","And remember... no witnesses."),
 'pay':speech("ROCKET: Heh... I heard the news.","BROCK won't be teaching anyone anymore.","Clean work, kid. Here's your pay."),
 'money':bytes(txt([["<PLAYER> received","¥10000!"]],0x50))+bytes([0x0b,0x06,0x50]),
 'invite':speech("You know... I like you, kid.","You've got what it takes to join TEAM ROCKET.",
                 "Go to CERULEAN CITY and take the test.","Then we'll see what you're really made of."),
 'after':speech("ROCKET: What are you waiting for?","Go to CERULEAN CITY and take the test."),
}
# ---- bank 32: logic + texts
C32=0x5800;T32=0x5a00
tx={};blob=bytearray()
for k,v in T.items():tx['t_'+k]=T32+len(blob);blob+=v
assert T32+len(blob)<0x6000
src=f"""
anykill:                         ; nz = some trainer was killed
    ld hl,$d4a4
    ld b,10
    xor a
.a: or [hl]
    inc hl
    dec b
    jr nz,.a
    ld hl,$d430
    ld b,32
.b: or [hl]
    inc hl
    dec b
    jr nz,.b
    ld hl,$d886
    or [hl]
    ret

vis106:                          ; museum 1F map script: hide the ROCKET (object 6) unless he belongs here
    ld a,[$d451]
    and a
    jr z,.hide
    ld a,[$d46c]
    and a
    jr nz,.hide
    ld a,[{STATE:#x}]
    and $0f
    cp 3
    jr nc,.hide
    call anykill
    ret nz
.hide:
    xor a
    ld [$c160],a
    ld a,$ff
    ld [$c264],a
    ld [$c265],a
    ret

rk106:                           ; the ROCKET's talk (text id 6)
    ld a,[{STATE:#x}]
    and $0f
    jr z,.first
    cp 1
    jr z,.one
    ld hl,{tx['t_after']:#x}
    jp {PRINTTEXT:#x}
.first:
    ld hl,{tx['t_intro']:#x}
    call {PRINTTEXT:#x}
    ld a,[$d4a5]
    bit 4,a
    jr z,.offer
    ld hl,{tx['t_already']:#x}
    call {PRINTTEXT:#x}
    jr .pay2
.offer:
    ld hl,{tx['t_contract']:#x}
    call {PRINTTEXT:#x}
    ld hl,{STATE:#x}
    ld a,[hl]
    and $f0
    or 1
    ld [hl],a
    ret
.one:
    ld a,[$d4a5]
    bit 4,a
    jr nz,.pay
    ld hl,{tx['t_remind']:#x}
    jp {PRINTTEXT:#x}
.pay:
    ld hl,{tx['t_pay']:#x}
    call {PRINTTEXT:#x}
.pay2:
    ld hl,$d347
    ld a,[hl]
    add 1
    daa
    jr nc,.ok
    ld a,$99
    ld [hl+],a
    ld [hl+],a
.ok:ld [hl],a
    ld hl,{tx['t_money']:#x}
    call {PRINTTEXT:#x}
    ld hl,{STATE:#x}
    ld a,[hl]
    and $f0
    or 2
    ld [hl],a
    ld hl,{tx['t_invite']:#x}
    jp {PRINTTEXT:#x}

wit106:                          ; PEWTER GYM map script: BROCK died under contract with his gym trainer alive -> NOTORIETY +5 (once)
    ld a,[{STATE:#x}]
    bit 6,a
    ret nz
    and $0f
    cp 1
    ret nz
    ld a,[$d4a5]
    bit 4,a
    ret z
    ld hl,{STATE:#x}
    set 6,[hl]
    bit 5,a
    ret nz
    ld a,[{NOTOR:#x}]
    add 5
    jr nc,.s
    ld a,$ff
.s: ld [{NOTOR:#x}],a
    ret

"""
old_ml=R[fo(0x2e,0x4000):fo(0x2e,0x4003)];assert old_ml[0]==0xc3;NEXT=old_ml[1]|old_ml[2]<<8
code,L=asm(src,C32,{})
assert C32+len(code)<=T32,len(code)
rom.put(fo(B32,C32),code,'Bank 32: v106 ROCKET (museum visibility, talk, witness check, map-load link)')
rom.put(fo(B32,T32),bytes(blob),'Bank 32: v106 ROCKET texts')
# map-load chain link (bank 2E, the chain jumps from link to link)
ML2E=0x7fc0
assert not any(R[fo(0x2e,ML2E):fo(0x2e,ML2E)+0x20])
ml2e,_=asm(f"""
    ld hl,{STATE:#x}
    ld a,[hl]
    and $0f
    cp 2
    jr nz,.n
    inc [hl]
.n: jp ${NEXT:04x}
""",ML2E,{})
rom.put(fo(0x2e,ML2E),ml2e,'Bank 2E: ml106 (map load: the paid ROCKET leaves the museum)')
rom.code(fo(0x2e,0x4000),bytes.fromhex('c3'+le(ML2E)),'Map-load chain: ml106 first',old_ml)

# ---- bank 17: museum 1F objects + text table + stubs, PEWTER GYM script wrapper
def hdr(mp):
    b=R[0xc23d+mp];h=fo(b,R[0x1ae+2*mp]|R[0x1af+2*mp]<<8);assert b==B17;return h
hm=hdr(MUS);tp=R[hm+5]|R[hm+6]<<8;sp=R[hm+7]|R[hm+8]<<8;op=R[hm+10]|R[hm+11]<<8
assert (tp,sp,op)==(0x412b,0x40f7,0x42c1),(hex(tp),hex(sp),hex(op))
o=fo(B17,op);nw=R[o+1];assert nw==5;p_=o+2+4*nw;ns=R[p_];assert ns==0;p_+=1;no=R[p_];assert no==5
objs_start=p_+1;q=objs_start
for i in range(no):
    e=R[q:q+8];q+=6 if not (e[5]&0xc0) else (8 if e[5]&0x40 else 7)
warpto=R[q:q+3*nw]
newobj=bytes([ROCKET,1+4,3+4,0xff,0xd0,6])
objdata=R[o:objs_start-1]+bytes([6])+R[objs_start:q]+newobj+warpto
AT=0x6000
assert not any(R[fo(B17,AT):fo(B17,AT)+0x100])
tab=R[fo(B17,tp):fo(B17,tp)+10]
s17,L17=asm(f"""
objs:
    db {','.join('$%02x'%x for x in objdata)}
texts:
    db {','.join('$%02x'%x for x in tab)}
    dw rktext
rktext:
    db $08
    ld hl,${L['rk106']:04x}
    ld b,${B32:02x}
    call ${BANKSW:04x}
    jp ${TEXTEND:04x}
musscr:
    ld hl,${L['vis106']:04x}
    ld b,${B32:02x}
    call ${BANKSW:04x}
    jp ${sp:04x}
""",AT,{})
rom.put(fo(B17,AT),s17,'Bank 17: v106 PEWTER MUSEUM 1F objects (+ROCKET), text table (+6), talk stub, map script wrapper')
rom.data(hm+5,bytes.fromhex(le(L17['texts'])+le(L17['musscr'])),'MUSEUM 1F text + script pointers -> v106',le(tp)+le(sp))
rom.data(hm+10,bytes.fromhex(le(L17['objs'])),'MUSEUM 1F object data -> v106 (+ROCKET)',le(op))
hg=hdr(GYM);gsp=R[hg+7]|R[hg+8]<<8;assert gsp==0x4387
AT2=AT+len(s17)
g17,LG=asm(f"""
gymscr:
    ld hl,${L['wit106']:04x}
    ld b,${B32:02x}
    call ${BANKSW:04x}
    jp ${gsp:04x}
""",AT2,{})
rom.put(fo(B17,AT2),g17,'Bank 17: v106 PEWTER GYM map script wrapper (witness check)')
rom.data(hg+7,bytes.fromhex(le(LG['gymscr'])),'PEWTER GYM script pointer -> v106 wrapper',le(gsp))
rom.finish('Creepy_Black_Mu_v106.gb','manifest_v106.json','CREEPY MU V106',extra=dict(labels={**{k:hex(v) for k,v in L.items()},**{k:hex(v) for k,v in L17.items()},**{k:hex(v) for k,v in tx.items()}}))
