# Creepy Black Mu v100 (on v99): the consort needs BADGES.
# AGATHA's stage 4: giving MISTY / ERIKA / SABRINA the HELIX FOSSIL (YES to "Give <NAME> the HELIX FOSSIL?") now checks
# the player's BADGES first (D356 bit count): ERIKA 4, MISTY 6, SABRINA all 8. Too few: she says she can't just be seen
# with anyone, only with a strong trainer who has proven themselves; she keeps nothing, the quest stays at stage 4,
# the player keeps the shell and can ask again later. Enough BADGES: her v16 reply and she joins, as before.
from patchlib import *
from patchguard import fo
V99_SHA='91f12bd1225367fe909e411886da0c694b71cf8d0bd6ca3bb6df1cd352b97dd2'
rom=Rom('Creepy_Black_Mu_v99.gb',V99_SHA)
R=bytes(rom.r)
PRINTTEXT=0x3c94;REMOVE_ITEM=0x6835;HELIX=0x2a;BADGES=0xd356
# name, v16 join_ label (2E), badges needed
GIRLS=[('MISTY',0x69e0,6),('ERIKA',0x6a23,4),('SABRINA',0x6a66,8)]
T={
 'MISTY':[["MISTY: Wait...","You want ME to","help you?"],["No way! I can't","just be seen with","anyone!"],
          ["I only go with a","strong trainer","who has proven","their skills!"],
          ["Come back when","you have six","BADGES!"]],
 'ERIKA':[["ERIKA: Oh my...","I am sorry."],["I cannot simply","be seen with just","anyone."],
          ["Only with a","strong trainer","who has shown","their abilities."],
          ["Perhaps when you","have four","BADGES..."]],
 'SABRINA':[["SABRINA: I saw","you asking me","this."],["But I cannot be","with just anyone."],
            ["Only a strong","trainer who has","proven their","power may stand","with me."],
            ["Return to me with","all eight","BADGES."]],
}
BASE=0x7d00
code=bytearray();lab={}
def here():return BASE+len(code)
# count: a = number of BADGES
lab['count']=here()
code+=bytes.fromhex('fa %02x %02x 06 08 0e 00'%(BADGES&255,BADGES>>8))   # ld a,[D356] / ld b,8 / ld c,0
code+=bytes.fromhex('0f 30 01 0c 05 20 f9 79 c9')                         # .l rrca / jr nc,+1 / inc c / dec b / jr nz,.l / ld a,c / ret
texts={}
stubs={}
for name,join,need in GIRLS:
    stubs[name]=here()
    c=lab['count']
    # call count / cp need / jr c,.no / ld a,HELIX / call remove_item / ret / .no: pop hl / ld hl,text / call PrintText / ret
    code+=bytes.fromhex('cd %02x %02x fe %02x 38 06 3e %02x cd %02x %02x c9'%(c&255,c>>8,need,HELIX,REMOVE_ITEM&255,REMOVE_ITEM>>8))
    texts[name]=len(code)+2;code+=bytes.fromhex('e1 21 00 00 cd %02x %02x c9'%(PRINTTEXT&255,PRINTTEXT>>8))
for name,join,need in GIRLS:
    t=here();code[texts[name]:texts[name]+2]=bytes([t&255,t>>8]);code+=txt(T[name],0x57)
assert BASE+len(code)<0x8000
rom.put(fo(0x2e,BASE),bytes(code),'Bank 2E: v100 consort BADGE check + refusal texts')
for name,join,need in GIRLS:
    s=stubs[name]
    rom.hook(fo(0x2e,join),bytes.fromhex('cd %02x %02x 00 00'%(s&255,s>>8)),'%s takes the HELIX FOSSIL only with %d BADGES'%(name,need),
             '3e %02x cd %02x %02x'%(HELIX,REMOVE_ITEM&255,REMOVE_ITEM>>8),provides=('a','f','b','c','d','e','h','l'))
rom.finish('Creepy_Black_Mu_v100.gb','manifest_v100.json','CREEPY MU V100',extra=dict(labels={k:hex(v) for k,v in stubs.items()}))
