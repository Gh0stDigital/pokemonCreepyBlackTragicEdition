# Shared helpers for build_v14.py and later. Every hook goes through the patch guard (patchguard.py), so a build
# refuses to produce a ROM when a hook
#   - overwrites bytes that other code jumps into (v1 0x29FD freeze), or
#   - leaves registers changed that the original code still reads / re-runs a replaced call with changed inputs
#     (v12 F:5033: every trainer killable).
#
#   from patchlib import *
#   rom=Rom('Creepy_Black_Mu_v13.gb',expect_sha=...)
#   rom.put(addr, code, 'name')                     # new code/data into verified-empty space
#   rom.hook(addr, call_bytes, 'name', old_hex, provides=('f',))   # AFTER the stub code is put
#   rom.code(addr, new_bytes, 'name', old_hex)      # other code edits (jump-target check only)
#   rom.data(addr, new_bytes, 'name', old_hex)      # tables, text, pics (no code checks)
#   rom.finish('Creepy_Black_Mu_v14.gb','manifest_v14.json','CREEPY MU V14', extra={...})
import json,hashlib,re
from pathlib import Path
from patchguard import check_hook,jumps_into,fo
ROOT=Path(__file__).resolve().parent

def le(a):return a.to_bytes(2,'little').hex()
def far(addr,bank):return '21 %s 06 %02x cd 18 36'%(le(addr),bank)

class Code:
    """tiny assembler: emit hex, labels, absolute refs and jr offsets"""
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

_cm={}
for k,v in re.findall(r'^\s*charmap "([^"]+)",\s*\$([0-9A-Fa-f]+)',(ROOT.parent/'pokeblack/charmap.asm').read_text(encoding='utf8'),re.M):_cm.setdefault(k,int(v,16))
def enc(s):
    out=bytearray()
    while s:
        k=next(k for k in sorted(_cm,key=len,reverse=True) if s.startswith(k));out.append(_cm[k]);s=s[len(k):]
    return out
def shown(line):return len(line.replace('#','POKé').replace('<PLAYER>','X'*7).replace('<RIVAL>','X'*7))
def txt(paras,end=0x58,maxw=17):
    """paragraphs of lines -> text bytes (lines <= 17 shown columns: the arrow uses column 18)"""
    out=bytearray([0])
    for i,p in enumerate(paras):
        if i:out.append(0x51)
        for j,line in enumerate(p):
            assert shown(line)<=maxw,line
            if j:out.append(0x4f if j==1 else 0x55)
            out+=enc(line)
    out.append(end);return out

class Rom:
    def __init__(self,path,expect_sha):
        src=(ROOT/path).read_bytes();assert hashlib.sha256(src).hexdigest()==expect_sha,'input ROM is not the verified one'
        self.input=path;self.input_sha=expect_sha;self.r=bytearray(src);self.log=[];self.reviews=[]
    def _apply(self,o,data,name,old):
        data=bytes(data);old=bytes.fromhex(old.replace(' ','')) if isinstance(old,str) else bytes(old)
        assert self.r[o:o+len(old)]==old,(name,hex(o),self.r[o:o+len(old)].hex())
        assert len(old)>=len(data),(name,'old bytes must cover the whole patch',len(old),len(data))
        self.log.append(dict(offset=hex(o),before=self.r[o:o+len(data)].hex(),after=data.hex(),name=name));self.r[o:o+len(data)]=data
    def put(self,o,data,name):
        assert not any(self.r[o:o+len(data)]),('not free',name,hex(o));self._apply(o,data,name,bytes(len(data)))
    def data(self,o,data,name,old):self._apply(o,data,name,old)
    def code(self,o,data,name,old,reviewed=None):
        hits=jumps_into(bytes(self.r),o,len(bytes(data)))
        if hits and not reviewed:
            raise SystemExit('REFUSED %s: other code jumps inside the patched bytes: %s'%(name,[(hex(s),hex(t)) for s,t in hits]))
        if hits:self.reviews.append((name,reviewed))
        self._apply(o,data,name,old)
    def hook(self,o,data,name,old,provides=(),reviewed=None):
        """call/jp to a stub that must already be in the ROM. provides = registers/flags the hook sets on purpose."""
        before=bytes(self.r);self._apply(o,data,name,old)
        probs=check_hook(before,bytes(self.r),o,len(bytes(data)),provides=provides)
        if probs and not reviewed:
            raise SystemExit('REFUSED hook %s at $%05x:\n  '%(name,o)+'\n  '.join(probs))
        if probs:self.reviews.append((name,reviewed,probs))
    def finish(self,out,manifest,ident,extra=None):
        r=self.r
        old_id=bytes(r[0x134:0x144]);r[0x134:0x144]=ident.encode().ljust(16,b'\0')
        self.log.append(dict(offset='0x134',before=old_id.hex(),after=bytes(r[0x134:0x144]).hex(),name='Branch identity'))
        v=0
        for x in r[0x134:0x14d]:v=(v-x-1)&255
        r[0x14d]=v;r[0x14e:0x150]=((sum(r[:0x14e])+sum(r[0x150:]))&65535).to_bytes(2,'big')
        assert len(r)==1048576
        (ROOT/out).write_bytes(r);sha=hashlib.sha256(r).hexdigest()
        (ROOT/manifest).write_text(json.dumps(dict(input=self.input,input_sha256=self.input_sha,sha256=sha,size=len(r),
            reviewed_guard_exceptions=[list(map(str,x)) for x in self.reviews],**(extra or {}),changes=self.log),indent=2))
        print('Built',out,sha);return sha
