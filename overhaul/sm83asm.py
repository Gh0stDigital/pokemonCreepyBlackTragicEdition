# Tiny SM83 (Game Boy CPU) assembler built from ref/instruction_set.py, for the v25+ builds.
#   from sm83asm import asm
#   code,labels = asm(SOURCE, org=0x4400, ext={'PrintText':0x3c94})
# Syntax (RGBDS-like): one instruction per line, `label:` / `.local:` labels, `; comment`, `db 1,2,"text"`, `dw label`,
# `ds n`, expressions with + - * & | << >> and symbols/`$hex`/`0xhex`. Operand forms follow the opcode table:
#   ld a,[$cf91]   ldh a,[$b4]   ld [hl+],a   ld a,[hl+]   jr nz,label   call label   bit 3,[hl]   swap a
# Macro: `farcall addr_or_label,bank`  ->  ld hl,addr / ld b,bank / call $3618  (the game's Bankswitch)
# Sizes never depend on operand values, so labels resolve in two passes.
import re,importlib.util
from pathlib import Path
_sp=importlib.util.spec_from_file_location('iset',Path(__file__).resolve().parent.parent/'ref'/'instruction_set.py')
_m=importlib.util.module_from_spec(_sp);_sp.loader.exec_module(_m)
BANKSWITCH=0x3618
def _norm(s):
    s=s.strip().lower();s=re.sub(r'\s+',' ',s);s=re.sub(r'\s*,\s*',',',s);s=re.sub(r'\[\s*','[',s);return re.sub(r'\s*\]',']',s)
_lit={};_pat=[]                         # literal patterns -> (opcode bytes) ; placeholder patterns
def _add(table,prefix):
    for op,txt in table.items():
        if txt.startswith('db ') or txt in ('CBPREFIX',):continue
        t=_norm(txt)
        if t=='rst vec':continue
        code=bytes([prefix,op]) if prefix else bytes([op])
        ph=re.findall(r'd8|d16|a8|a16|r8',t)
        if not ph:_lit[t]=code;continue
        if ph[0]=='r8' and t.startswith('jr'):ph=['rel8']
        rx='^'+re.escape(t).replace('pc\\+r8','(.+)').replace('sp\\+r8','sp\\+(.+)')
        rx=re.sub(r'd8|d16|a8|a16|r8','(.+?)',rx).replace('\\ ',' ')+'$'
        rx=rx.replace('(.+?)\\]','(.+?)\\]')
        _pat.append((re.compile(rx),code,ph[0] if ph else None,t))
_add(_m.instructions,0);_add(_m.cb_instructions,0xcb)
# prefer longest literal part first
_pat.sort(key=lambda x:-len(x[3]))
_SIZE={'d8':1,'a8':1,'r8':1,'rel8':1,'d16':2,'a16':2}
def _expr(s,syms,here):
    s=s.strip();s=re.sub(r'\$([0-9a-f]+)',r'0x\1',s,flags=re.I)
    def sub(m):
        n=m.group(0)
        if re.fullmatch(r'0x[0-9a-fA-F]+|\d+',n):return n
        if n=='@':return str(here)
        if n not in syms:raise KeyError(n)
        return str(syms[n])
    return int(eval(re.sub(r'0x[0-9a-fA-F]+|\d+|@|[A-Za-z_.][A-Za-z_0-9.]*',sub,s),{}))
def _split(src):
    out=[]
    for raw in src.splitlines():
        l=raw.split(';')[0].strip()
        if not l:continue
        while True:
            m=re.match(r'^([A-Za-z_.][A-Za-z_0-9.]*):\s*(.*)$',l)
            if not m:break
            out.append(('label',m.group(1)));l=m.group(2).strip()
        if l:out.append(('ins',l))
    return out
def _match(line):
    n=_norm(line)
    mr=re.match(r'^rst (.+)$',n)
    if mr:return bytes([0xc7+int(re.sub(r'^\$','0x',mr.group(1)),0)]),None,None
    if n in _lit:return _lit[n],None,None
    for rx,code,ph,t in _pat:
        m=rx.match(n)
        if m and ph:
            # reject register-looking captures
            if re.fullmatch(r'a|b|c|d|e|h|l|af|bc|de|hl|sp|\[hl\]',m.group(1).strip()):continue
            return code,ph,m.group(1)
    raise ValueError('cannot assemble: '+line)
def _items(line):                        # db/dw/ds operands (strings allowed)
    parts=[];cur='';q=False
    for ch in line:
        if ch=='"':q=not q;cur+=ch
        elif ch==',' and not q:parts.append(cur.strip());cur=''
        else:cur+=ch
    parts.append(cur.strip());return [p for p in parts if p]
def asm(src,org,ext=None):
    ext=dict(ext or {});items=_split(src)
    def run(syms,emit):
        pc=org;out=bytearray();last='';labels={}
        for kind,v in items:
            if kind=='label':
                name=v if not v.startswith('.') else last+v
                if not v.startswith('.'):last=v
                labels[name]=pc;continue
            low=v.lower()
            if low.startswith('farcall '):
                a,b=[x.strip() for x in v[8:].split(',')]
                seq=['ld hl,'+a,'ld b,'+b,'call %d'%BANKSWITCH]
                for s in seq:
                    code,ph,e=_match(s);pc+=len(code)+_SIZE.get(ph,0)
                    if emit:out+=_enc(code,ph,e,s,syms,pc,last)
                continue
            if low.startswith('db ') or low.startswith('dw ') or low.startswith('ds '):
                for it in _items(v[3:]):
                    if low.startswith('ds '):
                        n=_expr(it,syms,pc);pc+=n
                        if emit:out+=bytes(n)
                    elif it.startswith('"'):
                        b=it[1:-1].encode('latin1');pc+=len(b)
                        if emit:out+=b
                    elif low.startswith('db '):
                        pc+=1
                        if emit:out.append(_expr(_loc(it,last),syms,pc)&255)
                    else:
                        pc+=2
                        if emit:x=_expr(_loc(it,last),syms,pc);out+=bytes([x&255,x>>8&255])
                continue
            code,ph,e=_match(v);pc+=len(code)+_SIZE.get(ph,0)
            if emit:out+=_enc(code,ph,e,v,syms,pc,last)
        return out,labels
    _,lab=run(ext,False)
    allsyms={**ext,**lab}
    # local labels: also resolvable by bare name inside their scope (handled in _loc)
    out,_=run(allsyms,True)
    return bytes(out),lab
def _loc(e,last):                        # expand .local references to last_global.local
    return re.sub(r'(?<![A-Za-z_0-9.])(\.[A-Za-z_][A-Za-z_0-9]*)',lambda m:last+m.group(1),e)
def _enc(code,ph,e,line,syms,pc_after,last):
    if ph is None:return code
    val=_expr(_loc(e,last),syms,pc_after)
    if ph=='r8':
        if not -128<=val<128:raise ValueError('offset out of range: '+line)
        return code+bytes([val&255])
    if ph=='rel8':
        d=val-pc_after
        if not -128<=d<128:raise ValueError('jr out of range (%d): %s'%(d,line))
        return code+bytes([d&255])
    if ph=='a8':
        if val>=0xff00:val-=0xff00
        return code+bytes([val&255])
    if ph=='d8':
        if not -128<=val<256:raise ValueError('byte out of range: '+line)
        return code+bytes([val&255])
    return code+bytes([val&255,val>>8&255])
