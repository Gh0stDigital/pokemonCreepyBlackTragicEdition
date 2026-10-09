# RITUAL test ROM: same as build_v25_test.py but the built-in save is make_save_v25_ritual.py's (TOWER CHAMBER right after MR. MU's ritual).
# Creepy Black Mu v25 TEST ROM: v25 plus a built-in save. When the title menu finds no save in the cartridge RAM,
# it first unpacks the embedded game (GHOST route, CHARMANDER, just after the POKeDEX; made by make_save_v14.py)
# into SRAM bank 1, so CONTINUE starts there. NEW GAME still works; an existing save is never touched.
# The normal release stays Creepy_Black_Mu_v25.gb. The save (made on v14 by make_save_v14.py) only holds game RAM, which v15-v18 did not change.
from patchlib import *
from patchguard import fo
V25_SHA='8e06876abf0db4af57388b0319d0f169076470037bd6d305c96b0a5baa26c8e9'
rom=Rom('Creepy_Black_Mu_v25.gb',V25_SHA)
sav=(ROOT/'Creepy_Black_Mu_v25_ritual.sav').read_bytes();assert len(sav)==0x8000
LO,HI=0xa598,0xb523                                   # sGameData .. sMainDataCheckSum (all LoadSAV reads)
block=sav[0x2000+LO-0xa000:0x2000+HI-0xa000+1]
assert block[0:11].find(0x50)>0                       # player name present
def rle(b):                                           # 0 = end, 0x80|n = n copies of next byte, n = n literals
    out=bytearray();i=0;lit=bytearray()
    def flush():
        nonlocal lit
        if lit:out.extend(bytes([len(lit)])+lit);lit=bytearray()
    while i<len(b):
        j=i
        while j<len(b) and b[j]==b[i] and j-i<127:j+=1
        if j-i>=3:flush();out.extend([0x80|(j-i),b[i]]);i=j
        else:
            lit.append(b[i]);i+=1
            if len(lit)==127:flush()
    flush();out.append(0);return bytes(out)
def unrle(d):
    out=bytearray();i=0
    while d[i]:
        c=d[i];i+=1
        if c&0x80:out+=bytes([d[i]])*(c&0x7f);i+=1
        else:out+=d[i:i+c];i+=c
    return bytes(out)
packed=rle(block);assert unrle(packed)==block
g=Code(0x2e,0x6000)
g.label('install');g.emit('3e 0a ea 00 00 3e 01 ea 00 60 ea 00 40');g.ref('21','data');g.emit('11 98 a5')
g.label('lp');g.emit('2a a7');g.jr('28','done');g.emit('cb 7f');g.jr('20','run');g.emit('4f')
g.label('lit');g.emit('2a 12 13 0d');g.jr('20','lit');g.jr('18','lp')
g.label('run');g.emit('e6 7f 4f 2a')
g.label('rl');g.emit('12 13 0d');g.jr('20','rl');g.jr('18','lp')
g.label('done');g.emit('af ea 00 00 ea 00 60 c9')
g.label('data');g.raw(packed)
code=g.finish();assert 0x6000+len(code)<0x8000
rom.put(fo(0x2e,0x6000),code,'Bank 2E: built-in save (%d bytes packed from %d) + unpacker'%(len(packed),len(block)))
CHECKNAME=0x6077
b1=Code(1,0x7e00)
b1.label('menu');b1.emit('cd %s d8 '%le(CHECKNAME)+far(g.labels['install'],0x2e)+' c3 '+le(CHECKNAME))
rom.put(fo(1,0x7e00),b1.finish(),'Bank 1: no save -> install the built-in one')
rom.hook(fo(1,0x5ad6),'cd'+le(b1.labels['menu']),'Title menu: built-in save when the cartridge has none','cd'+le(CHECKNAME))
rom.finish('Creepy_Black_Mu_v25_ritual_test.gb','manifest_v25_ritual_test.json','CREEPY MU V25R',extra=dict(packed=len(packed)))
