# Creepy Black Mu v5: fossil back sprites made by altering the ORIGINAL Kabutops/Aerodactyl back
# sprites (bleached bone, kept outlines, wing membrane removed to the finger bones, spine + ribs).
# Replaces the v4 cropped-front sprites in place. On top of verified v4.
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parent
M4=json.loads((ROOT/'manifest_v4.json').read_text());V4_SHA=M4['sha256']
src=(ROOT/'Creepy_Black_Mu_v4.gb').read_bytes();assert hashlib.sha256(src).hexdigest()==V4_SHA
r=bytearray(src);log=[]
def patch(o,data,name,old):
    data=bytes(data);old=bytes(old)
    assert r[o:o+len(old)]==old,(name,hex(o))
    log.append(dict(offset=hex(o),before=r[o:o+len(data)].hex(),after=data.hex(),name=name));r[o:o+len(data)]=data
for name,bank,addr,v4file,v5file in (('Kabutops',0x0b,0x7f3c,'kab_back.bin','kab_back_v5.bin'),('Aerodactyl',0x0d,0x7e71,'aero_back.bin','aero_back_v5.bin')):
    old=(ROOT/v4file).read_bytes();new=(ROOT/v5file).read_bytes();o=bank*0x4000+addr-0x4000
    assert len(new)<=len(old)+sum(1 for b in r[o+len(old):(bank+1)*0x4000] if b==0)
    patch(o,new.ljust(len(old),b'\0'),'Fossil %s back sprite: fossilized original (%d bytes)'%(name,len(new)),old)
patch(0x134,b'CREEPY MU V5'.ljust(16,b'\0'),'Branch identity v5',b'CREEPY MU V4'.ljust(16,b'\0'))
v=0
for x in r[0x134:0x14d]:v=(v-x-1)&255
r[0x14d]=v;r[0x14e:0x150]=((sum(r[:0x14e])+sum(r[0x150:]))&65535).to_bytes(2,'big')
assert len(r)==1048576
out=ROOT/'Creepy_Black_Mu_v5.gb';out.write_bytes(r);sha=hashlib.sha256(r).hexdigest()
(ROOT/'manifest_v5.json').write_text(json.dumps(dict(input='Creepy_Black_Mu_v4.gb',input_sha256=V4_SHA,sha256=sha,size=len(r),changes=log),indent=2))
print('Built',out.name,sha)
