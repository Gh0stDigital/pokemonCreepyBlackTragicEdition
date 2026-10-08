# Creepy Black Mu v13: fix the v1 after-dialogue hook (Pokemon Center / Mart / vending freeze) and keep GHOST out
# of the Pokemon Center heal. Logged patches on top of verified Mu v12.
from pathlib import Path
import json,hashlib,re,io,sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'ref'));import pic
M12=json.loads((ROOT/'manifest_v12.json').read_text());V12_SHA=M12['sha256']
src=(ROOT/'Creepy_Black_Mu_v12.gb').read_bytes();assert hashlib.sha256(src).hexdigest()==V12_SHA
r=bytearray(src);log=[]
def patch(o,data,name,old):
    data=bytes(data);old=bytes.fromhex(old) if isinstance(old,str) else bytes(old)
    assert r[o:o+len(old)]==old,(name,hex(o),r[o:o+len(old)].hex())
    log.append(dict(offset=hex(o),before=r[o:o+len(data)].hex(),after=data.hex(),name=name));r[o:o+len(data)]=data
def put(o,data,name):            # write into verified-empty space
    assert not any(r[o:o+len(data)]),('not free',name,hex(o));patch(o,data,name,'00'*len(data))
def fo(bank,addr):return addr if bank==0 else bank*0x4000+addr-0x4000

class Code:
    def __init__(self,bank,org):self.bank=bank;self.org=org;self.b=bytearray();self.labels={};self.refs=[];self.rel=[]
    def emit(self,h):self.b+=bytes.fromhex(h)
    def raw(self,b):self.b+=bytes(b)
    def label(self,n):self.labels[n]=self.org+len(self.b)
    def ref(self,op,n):self.emit(op);self.refs.append((len(self.b),n));self.b+=b'\0\0'
    def jr(self,op,n):self.emit(op);self.rel.append((len(self.b),n));self.b+=b'\0'
    def finish(self,ext={}):
        L={**ext,**self.labels}
        for p,n in self.refs:self.b[p:p+2]=L[n].to_bytes(2,'little')
        for p,n in self.rel:
            d=L[n]-(self.org+p+1);assert -128<=d<128,n;self.b[p]=d&255
        return bytes(self.b)
def le(a):return a.to_bytes(2,'little').hex()
def far(addr,bank):return '21 %s 06 %02x cd 18 36'%(le(addr),bank)

cm={}
for k,v in re.findall(r'^\s*charmap "([^"]+)",\s*\$([0-9A-Fa-f]+)',(ROOT.parent/'pokeblack/charmap.asm').read_text(encoding='utf8'),re.M):cm.setdefault(k,int(v,16))
def enc(s):
    out=bytearray()
    while s:
        k=next(k for k in sorted(cm,key=len,reverse=True) if s.startswith(k));out.append(cm[k]);s=s[len(k):]
    return out







ADDNTIMES,BANKSWITCH=0x3abb,0x3618
GHOST=0x1f
POLICE=0x4200   # v2 police bulletin routine (bank 2E): checks wDoNotWait / wEnteringCableClub itself, then waits for a button

# 1. Bug fix. v1 replaced the 15 bytes at 0x29FD (end of DisplayTextID) with a far call + padding. But 0x2A03 is
#    AfterDisplayingTextID, the entry the Pokemon Center nurse, Poke Mart, vending machines and cable club jump to
#    (jr at 0x29E5/0x29F8, jp at 0x2A7F/0x2ABA/0x2AC5). Since v1 that address held the 2nd byte of "call Bankswitch"
#    ("18 36" = jr +$36), so after those dialogues the CPU jumped into the middle of CloseTextDisplay and crashed.
#    Restore the original first check at 0x29FD and start the far call exactly at 0x2A03.
patch(0x29fd,bytes.fromhex('fa 3c cc a7 20 09'+' 21 %s 06 2e cd %s'%(le(POLICE),le(BANKSWITCH))+' 00'),
      'Fix v1 hook: AfterDisplayingTextID (0x2A03) is a real entry again','2100420'+'62ecd1836'+'00'*7)

# 2. Pokemon Center: GHOST is taken out of the party while the nurse heals (not healed, no ball on the machine)
#    and put back in the same slot right after the healing animation. Done in RAM: GHOST is swapped to the last
#    slot and the party count is lowered by one, then everything is undone. (Not done if GHOST is the only one.)
n=Code(1,0x7c70)
n.label('swap_entry')                     # hl = table base, c = entry size: swap entries [D457] and [D458]
n.emit('e5 c5 fa 57 d4 06 00 cd %s 54 5d c1 e1 c5 fa 58 d4 06 00 cd %s c1'%(le(ADDNTIMES),le(ADDNTIMES)))
n.label('swl');n.emit('1a 47 7e 12 70 23 13 0d');n.jr('20','swl');n.emit('c9')
n.label('swap_gk')
for base,size in ((0xd164,1),(0xd16b,44),(0xd273,11),(0xd2b5,11)):
    n.emit('21 %s 0e %02x'%(le(base),size));n.ref('cd','swap_entry')
n.emit('c9')
n.label('hide');n.emit('3e ff ea 57 d4 fa 63 d1 fe 02 d8')            # nothing to do with < 2 Pokemon
n.emit('3d ea 58 d4 21 64 d1 0e 00')                                      # D458 = last slot
n.label('find');n.emit('2a fe ff c8 fe %02x'%GHOST);n.jr('28','found');n.emit('0c');n.jr('18','find')
n.label('found');n.emit('79 ea 57 d4');n.ref('cd','swap_gk')
n.emit('fa 58 d4 ea 63 d1 4f 06 00 21 64 d1 09 36 ff c9')                 # count = last slot, list ends there
n.label('show');n.emit('fa 57 d4 fe ff c8 fa 58 d4 4f 3c ea 63 d1 06 00 21 64 d1 09 36 %02x 23 36 ff'%GHOST)
n.ref('cd','swap_gk');n.emit('3e ff ea 57 d4 c9')
n.label('nurse');n.ref('cd','hide');n.emit('c3 50 7c')                    # then the v9 nurse heal (skip PRETA/AZHI)
n.label('anim');n.emit('06 1c 21 65 44 cd %s'%le(BANKSWITCH));n.ref('c3','show')   # AnimateHealingMachine, then GHOST back
code1=n.finish();put(fo(1,0x7c70),code1,'Bank 1: Pokemon Center keeps GHOST out of the heal')
patch(fo(1,0x7016),bytes.fromhex('cd'+le(n.labels['nurse'])),'Nurse heal -> hide GHOST first','cd507c')
patch(fo(1,0x701b),bytes.fromhex('cd'+le(n.labels['anim'])+'0000000000'),'Healing machine animation, then put GHOST back','061c216544cd1836')

# 3. Bug fix (v12). F:5033 is "call CompareHLWithBC" with hl = the trainer's header pointer and bc = 0 (z = no
#    header = scripted trainer -> "But, it failed!"). v12 routed it through a far call, which overwrote hl/b, so
#    EVERY trainer (gym leaders, Giovanni, the Champion...) became killable. Do the check in home bank space instead,
#    with the registers untouched: only BLUE's RIVAL1/RIVAL2 classes are turned into "killable" (-> GHOST hesitates).
RIVAL1,RIVAL2=25,42
h=Code(0,0xed)
h.label('kb');h.emit('cd 5c 36 c0 fa 31 d0 fe %02x'%RIVAL1);h.jr('28','rv');h.emit('fe %02x'%RIVAL2);h.jr('20','no')
h.label('rv');h.emit('a7 c9')
h.label('no');h.emit('af c9')
code0=h.finish();assert 0xed+len(code0)<=0x100;put(0xed,code0,'Home: trainer-curse "killable" check (BLUE only), registers kept')
M12L=json.loads((ROOT/'manifest_v12.json').read_text())
kb12=[c for c in M12L['changes'] if c['name'].startswith('Trainer CURSE: BLUE counts')][0]['after']
patch(fo(0xf,0x5033),bytes.fromhex('cd'+le(h.labels['kb'])),'Trainer CURSE check -> home (fix v12 register clobber)',kb12)

# Header -----------------------------------------------------------------------
patch(0x134,b'CREEPY MU V13'.ljust(16,b'\0'),'Branch identity v13',b'CREEPY MU V12'.ljust(16,b'\0'))
v=0
for x in r[0x134:0x14d]:v=(v-x-1)&255
r[0x14d]=v;r[0x14e:0x150]=((sum(r[:0x14e])+sum(r[0x150:]))&65535).to_bytes(2,'big')
assert len(r)==1048576
out=ROOT/'Creepy_Black_Mu_v13.gb';out.write_bytes(r);sha=hashlib.sha256(r).hexdigest()
(ROOT/'manifest_v13.json').write_text(json.dumps(dict(input='Creepy_Black_Mu_v12.gb',input_sha256=V12_SHA,sha256=sha,size=len(r),
  labels={'bank1':{k:hex(v) for k,v in n.labels.items()}},changes=log),indent=2))
print('Built',out.name,sha,'| bank1',len(code1))
