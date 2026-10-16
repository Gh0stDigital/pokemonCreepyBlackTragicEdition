# Creepy Black Mu v73: five small story/dialogue changes.
#   1. PRETA's sight: when PRETA (not the SILPH SCOPE item) unveils the ghost on POKeMON TOWER 6F, the battle text says so:
#      "PRETA's sight / unveiled the / GHOST's identity!" instead of "SILPH SCOPE unveiled the GHOST's identity!".
#   2. AGATHA with MR. FUJI on Tower 7F (before the rescue): no more "tied me up".
#   3. MR. FUJI at home, talked to again after the rescue (GHOST route, AGATHA not gone, not BLACK): he says AGATHA is still in the TOWER and may have something for you.
#   4. The SAFFRON shamaness no longer stands at SILPH CO.'s door: (y22,x19) -> (y24,x32), the open square in the south-east (she still replaces the town's last guard slot).
#   5. SNORLAX (ROUTE 12 / ROUTE 16): if CURSE was used in the battle, the "returned to the mountains" text is skipped (the script's flags still happen).
import json
from patchlib import *
from patchguard import fo
from sm83asm import asm

V72_SHA='7a7ba17160c90ad23dd484c8c76213ad6ebadd447c33767b2d002fbeed6e27a2'
rom=Rom('Creepy_Black_Mu_v72.gb',V72_SHA)
R=bytes(rom.r)
B32=0x32;TX32=0x5000
def T(paras,end=0x58):return bytes(txt(paras,end,17))
# ---------------------------------------------------------------- texts (bank 32)
TXTS={
 'preta':T([["PRETA's sight","unveiled the","GHOST's identity!"]]),
 'fuji':T([["MR.FUJI: Has my","FLUTE helped you?"],["AGATHA is still","in the TOWER."],["She may have","something to give","you as thanks","too."]],0x57)}
tx=bytearray();TA={}
for k,v in TXTS.items():TA[k]=TX32+len(tx);tx+=v
assert not any(R[fo(B32,TX32):fo(B32,TX32)+len(tx)]) and TX32+len(tx)<0x6000
rom.put(fo(B32,TX32),bytes(tx),'Bank 32: v73 texts (PRETA unveils the ghost, FUJI mentions AGATHA)')
# ---------------------------------------------------------------- 1. PRETA's text (bank 16)
A16=0x6800
assert not any(R[fo(0x16,A16):fo(0x16,A16)+64])
src16=f'''
pretatxt:                        ; replaces  ld hl,$4e4f  (the "SILPH SCOPE unveiled the GHOST's identity!" text): PRETA in the party -> its own text
    ld hl,$d164
.l: ld a,[hl+]
    cp $ff
    jr z,.orig
    cp $b6
    jr nz,.l
    ld hl,preta_far
    ret
.orig:
    ld hl,$4e4f
    ret
preta_far:
    db $17,{TA['preta']&255},{TA['preta']>>8},{B32},$50
snorlax:                         ; replaces  call DisplayTextID  after the SNORLAX battle: CURSE used = no "returned to the mountains"
    ld a,[$d452]
    and a
    ret nz
    jp $294d
'''
c16,L16=asm(src16,A16,{})
rom.put(fo(0x16,A16),c16,'Bank 16: v73 PRETA unveils text + SNORLAX cursed stub')
o=fo(0x16,0x4e0d);assert R[o:o+3].hex()=='214f4e'
rom.hook(o,bytes([0xcd,L16['pretatxt']&255,L16['pretatxt']>>8]),'Ghost unveiled text: PRETA\'s own text','214f4e',provides=('h','l'),
         reviewed='the stub only returns the text pointer in hl, like the replaced ld hl,imm16; a is clobbered (the next instruction is call PrintText)')
for site,a in ((0x5661,0x0e),(0x59a5,0x0b)):
    o=fo(0x16,site);assert R[o:o+3].hex()=='cd4d29' and R[o-4:o].hex()=='3e%02xe08c'%a,hex(site)
    rom.hook(o,bytes([0xcd,L16['snorlax']&255,L16['snorlax']>>8]),'SNORLAX after battle %04x: text unless CURSE was used'%site,'cd4d29',
             reviewed='the stub ends in the original jp DisplayTextID or returns; nothing after the call reads a register')
# ---------------------------------------------------------------- 2. AGATHA's hostage line (bank 2E, in place)
s=fo(0x2e,0x6a7c);old=R[s:s+84];assert old[0]==0 and old[-1]==0x58 and old[1:14]==enc('AGATHA: Hmph!')
new=T([["AGATHA: Hmph!","These ROCKET","brats got me"],["and old FUJI!","Get rid of them,","child!"]])
assert len(new)<=84,len(new)
rom.data(s,new+bytes(84-len(new)),'AGATHA\'s hostage speech without "tied me up"',old.hex())
# ---------------------------------------------------------------- 3. FUJI at home (bank 7): the after-flute talk
A7=0x772b
assert not any(R[fo(7,A7):fo(7,A7)+40])
src7=f'''
fujitxt:                         ; replaces  ld hl,$5970 (TX_FAR "Has my FLUTE helped you?"): GHOST route, AGATHA still there, not BLACK -> the longer text
    ld a,[$d451]
    and a
    jr z,.orig
    ld a,[$d46c]
    and a
    jr nz,.orig
    ld a,[$d466]
    bit 1,a
    jr nz,.orig
    ld hl,fuji_far
    ret
.orig:
    ld hl,$5970
    ret
fuji_far:
    db $17,{TA['fuji']&255},{TA['fuji']>>8},{B32},$50
'''
c7,L7=asm(src7,A7,{})
assert len(c7)<=40
rom.put(fo(7,A7),c7,'Bank 7: v73 FUJI mentions AGATHA')
o=fo(7,0x5953);assert R[o:o+3].hex()=='217059'
rom.hook(o,bytes([0xcd,L7['fujitxt']&255,L7['fujitxt']>>8]),'FUJI at home, after the FLUTE: text chooser','217059',provides=('h','l'),
         reviewed='returns the text pointer in hl like the replaced ld hl,imm16; the jr nz,$5953 above still lands on the (now call) instruction')
# ---------------------------------------------------------------- 4. the SAFFRON shamaness
L66={k:int(v,16) for k,v in json.load(open('manifest_v66.json'))['labels']['bank31'].items()}
t=fo(0x31,L66['tab66'])+7*7
assert list(R[t:t+7])==[10,26,23,64,128,7,1]
rom.data(t+1,bytes([24+4,32+4]),'SAFFRON shamaness: (y22,x19) at SILPH CO.\'s door -> (y24,x32)',bytes([26,23]).hex())
rom.finish('Creepy_Black_Mu_v73.gb','manifest_v73.json','CREEPY MU V73')
