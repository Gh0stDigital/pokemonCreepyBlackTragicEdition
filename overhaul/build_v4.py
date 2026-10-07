# Creepy Black Mu v4: real back sprites for Fossil Kabutops / Fossil Aerodactyl (cropped 1:1 from
# their front fossil art, mirrored, 4x4 tiles like every Gen-1 back sprite). On top of verified v3.
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parent
M3=json.loads((ROOT/'manifest_v3.json').read_text());V3_SHA=M3['sha256']
src=(ROOT/'Creepy_Black_Mu_v3.gb').read_bytes();assert hashlib.sha256(src).hexdigest()==V3_SHA
r=bytearray(src);log=[]
def patch(o,data,name,old):
    data=bytes(data);old=bytes.fromhex(old) if isinstance(old,str) else bytes(old)
    assert r[o:o+len(old)]==old,(name,hex(o),r[o:o+len(old)].hex())
    log.append(dict(offset=hex(o),before=r[o:o+len(data)].hex(),after=data.hex(),name=name));r[o:o+len(data)]=data
def fo(bank,addr):return bank*0x4000+addr-0x4000
def le(a):return a.to_bytes(2,'little')
# The sprite bank is chosen by species: B6 -> bank 0B, B7 -> bank 0D (UncompressMonSprite).
for name,bank,addr,lab,front in (('kab',0x0b,0x7f3c,'kab_data',0x79e8),('aero',0x0d,0x7e71,'aero_data',0x6536)):
    pic=(ROOT/(name+'_back.bin')).read_bytes();o=fo(bank,addr)
    assert not any(r[o:o+len(pic)]) and addr+len(pic)<=0x8000,(name,'no room')
    patch(o,pic,'Fossil %s back sprite (%d bytes)'%(name,len(pic)),'00'*len(pic))
    hdr=fo(0x0e,int(M3['labels']['bankE'][lab],16))+9          # back-pic pointer inside the custom header
    patch(hdr,le(addr),'Fossil %s header back pointer -> new sprite'%name,le(front))
patch(0x134,b'CREEPY MU V4'.ljust(16,b'\0'),'Branch identity v4',b'CREEPY MU V3'.ljust(16,b'\0'))
v=0
for x in r[0x134:0x14d]:v=(v-x-1)&255
r[0x14d]=v;r[0x14e:0x150]=((sum(r[:0x14e])+sum(r[0x150:]))&65535).to_bytes(2,'big')
assert len(r)==1048576
out=ROOT/'Creepy_Black_Mu_v4.gb';out.write_bytes(r);sha=hashlib.sha256(r).hexdigest()
(ROOT/'manifest_v4.json').write_text(json.dumps(dict(input='Creepy_Black_Mu_v3.gb',input_sha256=V3_SHA,sha256=sha,size=len(r),changes=log),indent=2))
print('Built',out.name,sha)
