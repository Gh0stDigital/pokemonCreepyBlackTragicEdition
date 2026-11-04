# Creepy Black Mu v105 (on v104): the legendary birds after the ritual, and fixed METAMORPHOSIS forms for the story trainers.
#  1. As BLACK (D46C) the three legendary birds are gone from their places (PROF. OAK has caught them): bird105 (2E:7F80), the new first link of
#     the 2E:4000 map-load chain, sets their show/hide bits (ZAPDOS POWER PLANT toggle 85 = D5B0 bit 5, MOLTRES VICTORY ROAD 2F toggle 91 =
#     D5B1 bit 3, ARTICUNO SEAFOAM B4F toggle 227 = D5C2 bit 3). Their "fought" flags are not touched.
#  2. PROF. OAK's final party (class 26, party 2: MR. MIME, VENUSAUR, ARTICUNO, ZAPDOS, MOLTRES, MEW) leaves out every bird the player had
#     already fought before (killed or caught; the bird's trainer-header flag: ZAPDOS D7D4 bit 1, MOLTRES D7EE bit 6, ARTICUNO D882 bit 2):
#     oak105 (E:7F20) in front of v45's ReadTrainer stub at E:5CE6 returns without AddPartyMon for such a bird.
#  3. METAMORPHOSIS in the trainer phase turns these trainers into a fixed POKeMON instead of a random uncaught one: LORELEI -> GOLDEEN,
#     BRUNO -> GOLEM, LANCE -> CHARIZARD, BLUE (champion class 2B) -> FEAROW, BILL (class 26 party 1) -> MR. MIME. meta105 (2F:5F00) replaces
#     bane_phase's call rand_uncaught (2F:4159); everyone else (PROF. OAK too) still gets a random one.
from patchlib import *
from patchguard import fo
from sm83asm import asm
V104_SHA='4b95c500d9620d43c2a5b63da4644ecba39ed87417929e5648fa1ec6edb49778'
rom=Rom('Creepy_Black_Mu_v104.gb',V104_SHA)
R=bytes(rom.r)
NAMES=0x1c21e
def spname(s):return R[NAMES+10*(s-1):NAMES+10*s].split(b'\x50')[0]
def enc(t):return bytes(0xe8 if c=='.' else 0x80+ord(c)-65 for c in t)
SP={n:s for n,s in (('GOLDEEN',0x9d),('GOLEM',0x31),('CHARIZARD',0xb4),('FEAROW',0x23),('MR.MIME',0x2a),('ZAPDOS',0x4b),('MOLTRES',0x49),('ARTICUNO',0x4a))}
for n,s in SP.items():assert spname(s)==enc(n),(n,hex(s))
LORELEI,BRUNO,LANCE,BLUE3,BILLCLS=0x2c,0x21,0x2f,0x2b,26        # BILL / PROF.OAK = class 26 DECIMAL ($1A)
le=lambda a:'%02x %02x'%(a&255,a>>8)

# ---- 1. birds hidden as BLACK (map-load chain)
B1=0x7f80
old=R[fo(0x2e,0x4000):fo(0x2e,0x4003)];assert old[0]==0xc3;nxt=old[1]|old[2]<<8
# trainer headers: the flags the bird fights set (checked here so the numbers below are the real ones)
for b,a,flag in ((7,0x636b,(0xd7d3,9)),(0x14,0x5871,(0xd7ee,6)),(0x11,0x6886,(0xd882,2))):
    h=R[fo(b,a):fo(b,a)+4];assert (h[2]|h[3]<<8,h[0])==flag,h.hex()
bird=bytes.fromhex('fa 6c d4 a7 28 0f 21 b0 d5 cb ee 21 b1 d5 cb de 21 c2 d5 cb de c3 '+le(nxt))
rom.put(fo(0x2e,B1),bird,'Bank 2E: bird105 (map load: legendary birds hidden as BLACK)')
rom.code(fo(0x2e,0x4000),bytes.fromhex('c3 '+le(B1)),'Map-load chain: bird105 first',old)

# ---- 2. OAK leaves out birds the player already fought
B2=0x7f20;V45=0x7ee0
assert R[fo(0xe,0x5ce6):fo(0xe,0x5ce9)].hex()=='cde07e' and R[fo(0xe,V45):fo(0xe,V45)+2].hex()=='e521'
oak,_=asm(f"""
oak105:
    ld a,[$d031]
    cp ${BILLCLS:02x}
    jr nz,.go
    ld a,[$d05d]
    cp 2
    jr nz,.go
    ld a,[$cf91]
    cp ${SP['ZAPDOS']:02x}
    jr nz,.m
    ld a,[$d7d4]
    bit 1,a
    ret nz
    jr .go
.m: cp ${SP['MOLTRES']:02x}
    jr nz,.a
    ld a,[$d7ee]
    bit 6,a
    ret nz
    jr .go
.a: cp ${SP['ARTICUNO']:02x}
    jr nz,.go
    ld a,[$d882]
    bit 2,a
    ret nz
.go:jp ${V45:04x}
""",B2,{})
rom.put(fo(0xe,B2),oak,'Bank E: oak105 (PROF. OAK skips birds the player already fought)')
rom.code(fo(0xe,0x5ce6),bytes.fromhex('cd '+le(B2)),'ReadTrainer (special format): AddPartyMon -> oak105 -> v45 stub','cd e0 7e')

# ---- 3. METAMORPHOSIS forms
B3=0x5f00;RAND=0x41af
assert R[fo(0x2f,0x4159):fo(0x2f,0x415c)].hex()=='cdaf41'
tab=[(LORELEI,0,'GOLDEEN'),(BRUNO,0,'GOLEM'),(LANCE,0,'CHARIZARD'),(BLUE3,0,'FEAROW'),(BILLCLS,1,'MR.MIME')]
code,_=asm(f"""
meta105:                         ; a = the species the trainer turns into (fixed for story trainers, else random uncaught)
    ld a,[$d031]
    ld c,a
    ld hl,tab
.l: ld a,[hl+]
    cp $ff
    jp z,${RAND:04x}
    cp c
    jr nz,.s2
    ld a,[hl+]
    and a
    jr z,.ok
    ld b,a
    ld a,[$d05d]
    cp b
    jr nz,.s1
.ok:ld a,[hl]
    ret
.s2:inc hl
.s1:inc hl
    jr .l
tab:
"""+''.join("    db ${:02x},{},${:02x}\n".format(c,n,SP[x]) for c,n,x in tab)+"    db $ff\n",B3,{})
rom.put(fo(0x2f,B3),bytes(code),'Bank 2F: meta105 (fixed METAMORPHOSIS forms for LORELEI/BRUNO/LANCE/BLUE/BILL)')
rom.code(fo(0x2f,0x4159),bytes.fromhex('cd '+le(B3)),'bane_phase: rand_uncaught -> meta105','cd af 41')
rom.finish('Creepy_Black_Mu_v105.gb','manifest_v105.json','CREEPY MU V105',extra=dict(labels=dict(bird105=hex(B1),oak105=hex(B2),meta105=hex(B3))))
