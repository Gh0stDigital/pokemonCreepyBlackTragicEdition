# Audit: find jr/jp/call instructions whose target lands strictly inside a code range our patches overwrote.
# Run from overhaul/: python ../ref/patch_jump_audit.py  (expects false positives from data bytes; read each hit)
# For every patch that overwrote existing (nonzero) bytes, find jr/jp/call instructions anywhere in the
# same bank (or home) whose target lands strictly inside the patched range.
import json,glob,sys
r=open('Creepy_Black_Mu_v13.gb','rb').read()
patches=[]
v1=[(0x18e5b,7,'v1 Pallet script hook'),(0xce2a,3,'v1 map hook'),(0xcd99,3,'v1 kill hook'),(0x1ce27,5,'v1 rival award hook'),
    (0x1d210,16,'v1 remove pre-battle Ghost award'),(0x525af,5,'v1 battle init hook'),(0x3d723,3,'v1 curse track'),(0x3c6e3,3,'v1 defeat text'),
    (0x29fd,15,'v1 police/after-text hook'),(0xfbc9,6,'v1 NEW GAME clear')]
for o,n,name in v1:patches.append(('v1',o,n,name))
for f in ['manifest_v%d.json'%i for i in range(2,14)]:
    m=json.load(open(f))
    for c in m['changes']:
        o=int(c['offset'],16);b=bytes.fromhex(c['before']);a=bytes.fromhex(c['after'])
        bad=('identity','name','sprite','pic','text','Text','class','party','Species','Move data','dex','cry','Cry','header','Rewrap','pointer','table','Bank ','Repoint','moves','Mirage trainer','Remove move','Dex')
        if any(b) and len(a)>=2 and not any(k in c['name'] for k in bad):patches.append((f,o,len(a),c['name']))
def cpu(o):return o if o<0x4000 else 0x4000+o%0x4000
JR={0x18,0x20,0x28,0x30,0x38};JP={0xc3,0xc2,0xca,0xd2,0xda,0xcd,0xc4,0xcc,0xd4,0xdc}
hits=[]
for f,o,n,name in patches:
    bank=o//0x4000;lo=cpu(o);hi=lo+n
    regions=[(0,0x4000)] if bank==0 else [(bank*0x4000,bank*0x4000+0x4000),(0,0x4000)]
    if bank==0:regions=[(i*0x4000,i*0x4000+0x4000) for i in range(64)]   # home code is reachable from every bank
    for s,e in regions:
        for i in range(s,e-2):
            op=r[i]
            if op in JR:
                t=cpu(i)+2+(r[i+1]-256 if r[i+1]>127 else r[i+1])
                if (i//0x4000==o//0x4000 or bank==0 and i<0x4000) and lo<t<hi:hits.append((f,name,hex(o),'jr from',hex(i),hex(t)))
            elif op in JP:
                t=r[i+1]|r[i+2]<<8
                if lo<t<hi and (bank==0 or t>=0x4000):hits.append((f,name,hex(o),'jp/call from',hex(i),hex(t)))
from collections import defaultdict
g=defaultdict(list)
for h in hits:g[(h[0],h[1],h[2])].append(h[3:])
for k,v in g.items():print(k,len(v),v[:6])
for f,o,n,name in patches:print('  checked',f,hex(o),n,name)
print(len(patches),'code-overwriting patches checked;',len(hits),'candidate mid-patch jumps')
