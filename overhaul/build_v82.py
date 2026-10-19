# Creepy Black Mu v82: when METAMORPHOSIS (or a picked-up black ball) adds a POKeMON, the text is "<MON> was ensnared!" (was "<MON> joined your party." /
#   "<MON> was sent to the PC."). Box case: "<MON> was ensnared!" + "It was sent to the PC.". The two old texts (2F:420C / 2F:4224) become TX_FAR to bank 31.
from patchlib import *
from patchguard import fo
from sm83asm import asm

V81_SHA='8fba6e3b472e39afc76593a3f9cf389409cde07a9a511d058b0b0478598ba63d'
rom=Rom('Creepy_Black_Mu_v81.gb',V81_SHA)
R=bytes(rom.r)
NAME=0xcd6d
def rt(*parts):
    out=bytearray();inside=False
    for p in parts:
        if isinstance(p,tuple):
            if inside:out.append(0x50);inside=False
            out+=bytes([1,p[1]&255,p[1]>>8])
        else:
            if not inside:out.append(0);inside=True
            out+={'line':b'\x4f','cont':b'\x55','para':b'\x51'}.get(p,None) or enc(p)
    if not inside:out.append(0)
    out+=b'\x58';return bytes(out)
OLDP=rt(('ram',NAME),'line','joined your party.');OLDB=rt(('ram',NAME),'line','was sent to the PC.')
for s in ('was ensnared!','It was sent to','the PC.'):assert len(s)<=17
NEWP=rt(('ram',NAME),'line','was ensnared!')
NEWB=rt(('ram',NAME),'line','was ensnared!','para','It was sent to','line','the PC.')
B31=0x31;TX=0x5800
assert not any(R[fo(B31,TX):fo(B31,TX)+0x80])
ap=TX;ab=TX+len(NEWP)
rom.put(fo(B31,TX),NEWP+NEWB,'Bank 31: v82 "was ensnared!" texts')
def at(old,new):
    o=R.find(old,fo(0x2f,0x4000),fo(0x2f,0x4400));assert o>=0 and R.find(old,o+1,fo(0x2f,0x4400))<0
    far=bytes([0x17])+bytes.fromhex(le(new))+bytes([B31,0x50])
    return o,far+bytes(len(old)-len(far))
o,n=at(OLDP,ap);rom.data(o,n,'give (party): "<MON> was ensnared!" (TX_FAR to bank 31)',OLDP.hex())
o,n=at(OLDB,ab);rom.data(o,n,'give (box): "<MON> was ensnared! It was sent to the PC." (TX_FAR to bank 31)',OLDB.hex())
rom.finish('Creepy_Black_Mu_v82.gb','manifest_v82.json','CREEPY MU V82')
