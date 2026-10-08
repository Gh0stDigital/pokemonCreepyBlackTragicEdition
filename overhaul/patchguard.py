# Patch guard: static checks that catch the two kinds of hook bugs this project has had.
#
#  1. jumps_into(rom, offset, length): every jr/jp/call/rst elsewhere in the ROM whose target lands strictly
#     inside the bytes we are about to overwrite (v1's 0x29FD hook covered the entry point 0x2A03 -> freeze).
#  2. check_hook(...): register safety of a hook that replaces original code with "call STUB" / "jp STUB":
#       a) registers the original code still reads after the patched bytes must not be left changed by the stub
#          (unless declared in provides=, i.e. the hook's intended result such as the zero flag);
#       b) when the stub re-runs a replaced "call X", the registers X reads must not have been changed by the
#          stub first (v12 F:5033: a far call clobbered hl/b before CompareHLWithBC -> every trainer killable).
#
# The analysis is a small SM83 decoder with path search: register reads/writes, constant tracking for the
# "ld hl,addr / ld b,bank / call Bankswitch" far-call pattern, push/pop restore, calls followed (depth-limited).
import sys,os
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','ref'))
from instruction_set import instructions,cb_instructions

BANKSWITCH=0x3618
PREDEF=0x3ec1      # Predef: input a = predef id; predef arguments travel through wPredefHL/DE/BC (not checked)
PAIRS={'af':('a','f'),'bc':('b','c'),'de':('d','e'),'hl':('h','l'),'sp':('sp',)}
REG8=('a','b','c','d','e','h','l')

def fo(bank,addr):return addr if addr<0x4000 else bank*0x4000+addr-0x4000

def regs_in(s):
    """registers named in an operand string"""
    s=s.replace('[','').replace(']','').replace('+','').replace('-','')
    if s in PAIRS:return set(PAIRS[s])
    if s in REG8:return {s}
    return set()

def decode(r,bank,addr):
    """-> dict(len, reads, writes, kind, target, cond, imm, text)"""
    o=fo(bank,addr);op=r[o]
    if op==0xcb:
        t=cb_instructions[r[o+1]];n=2
    else:
        t=instructions.get(op,'db');n=1
        if 'd16' in t or 'a16' in t:n=3
        elif 'd8' in t or 'a8' in t or 'r8' in t:n=2
    imm=None
    if n==3 and op!=0xcb:imm=r[o+1]|r[o+2]<<8
    elif n==2 and op!=0xcb:imm=r[o+1]
    mn=t.split(' ')[0];args=t[len(mn):].strip().split(',') if ' ' in t else []
    R,W=set(),set();kind='seq';target=None;cond=False
    if mn in ('ld','ldh'):
        dst,src=args
        if dst.startswith('['):
            R|=regs_in(dst);R|=regs_in(src)
            if 'hl+' in dst or 'hl-' in dst:W|={'h','l'}
        else:
            if src=='sp+r8':R|={'sp'};W|={'h','l','f'}
            else:
                R|=regs_in(src)
                if 'hl+' in src or 'hl-' in src:W|={'h','l'}
            W|=regs_in(dst)
    elif mn in ('inc','dec'):
        x=args[0];R|=regs_in(x)
        if x.startswith('['):W|={'f'}
        else:
            W|=regs_in(x)
            if x not in PAIRS:W|={'f'}
    elif mn in ('add','adc','sub','sbc','and','xor','or','cp'):
        if len(args)==2:d,s=args
        else:d,s='a',args[0]
        R|=regs_in(d)|regs_in(s)
        if mn in ('adc','sbc'):R|={'f'}
        if mn!='cp':W|=regs_in(d)
        W|={'f'}
    elif mn in ('rlca','rrca','rla','rra','daa','cpl'):
        R|={'a'};W|={'a','f'}
        if mn in ('rla','rra','daa'):R|={'f'}
        if mn=='cpl':W-={'f'};W|={'f'}
    elif mn in ('scf',):W|={'f'}
    elif mn=='ccf':R|={'f'};W|={'f'}
    elif mn=='push':R|=regs_in(args[0]);kind='push'
    elif mn=='pop':W|=regs_in(args[0]);kind='pop'
    elif mn in ('rlc','rrc','rl','rr','sla','sra','swap','srl'):
        x=args[0];R|=regs_in(x);W|={'f'}|(set() if x.startswith('[') else regs_in(x))
        if mn in ('rl','rr'):R|={'f'}
    elif mn=='bit':R|=regs_in(args[1]);W|={'f'}
    elif mn in ('res','set'):x=args[1];R|=regs_in(x);W|=set() if x.startswith('[') else regs_in(x)
    elif mn in ('jr','jp','call'):
        cond=len(args)==2
        if cond:R|={'f'}
        a=args[-1]
        if a=='hl':kind='jphl';R|={'h','l'}
        else:
            if mn=='jr':d=r[o+1];d=d-256 if d>127 else d;target=addr+2+d
            else:target=imm
            kind=mn
    elif mn in ('ret','reti'):
        cond=len(args)==1
        if cond:R|={'f'}
        kind='ret'
    elif mn=='rst':kind='bad' if op==0xff else 'call';target=op&0x38   # rst $38 (opcode ff) = runaway code
    elif mn in ('nop','di','ei','halt','stop'):pass
    else:kind='bad'
    return dict(len=n,reads=R,writes=W,kind=kind,target=target,cond=cond,imm=imm,text=t,op=op)

def expand(regs):
    out=set()
    for x in regs:out|=set(PAIRS.get(x,(x,)))
    return out

class Analyzer:
    """Path search over code. State = (dirty set, constants for h,l,b, push stack)."""
    def __init__(self,rom,max_steps=400,max_depth=4):
        self.r=rom;self.max_steps=max_steps;self.max_depth=max_depth

    def _reach(self,bank,addr):
        return addr<0x4000 or 0x4000<=addr<0x8000

    def live_in(self,bank,addr,depth=0,stop=None,_memo=None):
        """registers read before being written, on any path from addr (calls followed). Paths end at ret/jp hl/
        unreachable targets/step limit, or at an address in stop."""
        memo=_memo if _memo is not None else {}
        key=(bank,addr,depth)
        if key in memo:return memo[key]
        memo[key]=set()
        reads=set();seen=set()
        work=[(addr,frozenset(),())]       # (address, written regs, push stack of (pair, was-written))
        steps=0
        while work and steps<self.max_steps:
            a,W,stk=work.pop();steps+=1
            if (a,W,stk) in seen:continue
            seen.add((a,W,stk))
            if stop and a in stop:continue
            if not self._reach(bank,a):continue
            ins=decode(self.r,bank,a)
            if ins['kind']=='bad':continue
            k=ins['kind']
            if k=='push':                   # saving a register is not a use of its value
                pr=ins['text'].split()[1];work.append((a+1,W,stk+((pr,tuple(x for x in PAIRS[pr] if x in W)),)));continue
            if k=='pop' and stk:
                pr,was=stk[-1];W2=set(W)
                for x in PAIRS[ins['text'].split()[1]]:
                    W2.discard(x)
                    if x in was:W2.add(x)
                work.append((a+1,frozenset(W2),stk[:-1]));continue
            new=ins['reads']-W
            if new and getattr(self,'where',None) is not None:
                for x in new:self.where.setdefault(x,(bank,a,ins['text']))
            reads|=new
            if a<0x4000 and k in ('call','jp','jr') and ins['target'] is not None and ins['target']>=0x4000:
                # home code reaching banked addresses: the active bank is unknown here, so stop this path
                reads|=ins['reads']-W;continue
            if k=='call' and ins['target']==PREDEF:
                reads|={'a'}-W
                work.append((a+ins['len'],frozenset(W|{'a','b','c','d','e','h','l','f'}),stk));continue
            if k=='call' and depth<self.max_depth:
                t=ins['target']
                if t!=BANKSWITCH:
                    sub=self.live_in(bank,t,depth+1,_memo=memo)
                    reads|=sub-W
                W2=W|ins['writes']
                work.append((a+ins['len'],frozenset(W2|self.must_write(bank,t,depth+1) if t and t!=BANKSWITCH else W2),stk))
                continue
            W2=frozenset(W|ins['writes'])
            if k=='ret':
                if ins['cond']:work.append((a+1,W2,stk))
                continue
            if k=='jphl':continue
            if k in ('jr','jp'):
                if ins['cond']:work.append((a+ins['len'],W2,stk))
                work.append((ins['target'],W2,stk));continue
            work.append((a+ins['len'],W2,stk))
        memo[key]=reads
        return reads

    def must_write(self,bank,addr,depth=0,_memo=None):
        """registers written on every path from addr to a ret (approximate, used after calls)."""
        if addr is None or depth>self.max_depth:return set()
        res=None;steps=0;work=[(addr,frozenset())];seen=set()
        while work and steps<self.max_steps:
            a,W=work.pop();steps+=1
            if (a,W) in seen or not self._reach(bank,a):continue
            seen.add((a,W))
            ins=decode(self.r,bank,a);k=ins['kind']
            if k=='bad':continue
            W2=frozenset(W|ins['writes'])
            if k=='ret':
                res=set(W2) if res is None else res&W2
                if ins['cond']:work.append((a+1,W2))
                continue
            if k in ('jr','jp'):
                if ins['cond']:work.append((a+ins['len'],W2))
                work.append((ins['target'],W2));continue
            if k=='jphl':continue
            work.append((a+ins['len'],W2))
        return res or set()

    def may_write(self,bank,addr,depth=0,watch=None,dirty0=frozenset(),consts0=None):
        """registers a routine may leave changed at its return (push/pop restores honoured). Far calls through
        Bankswitch are followed using tracked constants. watch: {call_target: live_in regs} -> report every call
        to a watched target made while one of its inputs is dirty."""
        out=set();problems=[];steps=0
        start=(addr,bank,dirty0,(),tuple(sorted((consts0 or {}).items())))
        work=[start];seen=set()
        while work and steps<self.max_steps*4:
            a,bk,D,stack,cs=work.pop();steps+=1
            if (a,bk,D,stack,cs) in seen:continue
            seen.add((a,bk,D,stack,cs))
            if not self._reach(bk,a):continue
            consts=dict(cs);ins=decode(self.r,bk,a);k=ins['kind'];op=ins['op']
            if k=='bad':continue
            nD=set(D)|ins['writes']
            # constants for ld hl,d16 / ld b,d8 / ld a,d8 (far-call pattern)
            for reg in ins['writes']:consts.pop(reg,None)
            if op==0x21:consts['hl']=ins['imm']
            if op==0x06:consts['b']=ins['imm']
            if 'h' in ins['writes'] or 'l' in ins['writes']:
                if op!=0x21:consts.pop('hl',None)
            if k=='push':
                pr=ins['text'].split()[1];stack=stack+((pr,tuple(sorted(set(PAIRS[pr])&set(D)))),)
            elif k=='pop' and stack:
                pr,was=stack[-1];stack=stack[:-1]
                for x in PAIRS[ins['text'].split()[1]]:
                    nD.discard(x)
                    if x in was:nD.add(x)
            if k=='call':
                t=ins['target']
                if t==PREDEF:
                    if watch and t in watch and 'a' in D:problems.append('Predef call at %02x:%04x with a changed'%(bk,a))
                    nD|={'a','b','c','d','e','h','l','f'}
                    work.append((a+ins['len'],bk,frozenset(nD),stack,tuple(sorted(consts.items()))));continue
                if watch and t in watch:
                    bad=watch[t]&set(D)
                    if bad:problems.append('call $%04x at %02x:%04x with changed %s'%(t,bk,a,sorted(bad)))
                if t==BANKSWITCH and 'hl' in consts and 'b' in consts and depth<self.max_depth:
                    sub,pr=self.may_write(consts['b'],consts['hl'],depth+1,watch,frozenset(nD|{'a','b','h','l','f'}))
                    nD|=sub|{'a','b','f'};problems+=pr        # Bankswitch itself: a,b (and flags) changed
                elif t is not None and t!=BANKSWITCH and depth<self.max_depth:
                    sub,pr=self.may_write(bk,t,depth+1,watch,frozenset(nD));nD|=sub;problems+=pr
                else:nD|={'a','b','c','d','e','h','l','f'}  # unknown callee: assume everything
                work.append((a+ins['len'],bk,frozenset(nD),stack,tuple(sorted(consts.items()))));continue
            if k=='ret':
                out|=nD
                if ins['cond']:work.append((a+1,bk,frozenset(nD),stack,tuple(sorted(consts.items()))))
                continue
            if k=='jphl':out|=nD|{'a','b','c','d','e','h','l','f'};continue
            if k in ('jr','jp'):
                t=ins['target']
                if t==BANKSWITCH and 'hl' in consts and 'b' in consts and depth<self.max_depth:
                    if watch and t in watch:pass
                    sub,pr=self.may_write(consts['b'],consts['hl'],depth+1,watch,frozenset(nD|{'a','b','h','l','f'}))
                    out|=sub|{'a','b','f'};problems+=pr
                    if ins['cond']:work.append((a+ins['len'],bk,frozenset(nD),stack,tuple(sorted(consts.items()))))
                    continue
                if watch and t in watch:
                    bad=watch[t]&set(D)
                    if bad:problems.append('jp $%04x at %02x:%04x with changed %s'%(t,bk,a,sorted(bad)))
                if ins['cond']:work.append((a+ins['len'],bk,frozenset(nD),stack,tuple(sorted(consts.items()))))
                work.append((t,bk,frozenset(nD),stack,tuple(sorted(consts.items()))));continue
            work.append((a+ins['len'],bk,frozenset(nD),stack,tuple(sorted(consts.items()))))
        return out,problems

JR={0x18,0x20,0x28,0x30,0x38};JPC={0xc3,0xc2,0xca,0xd2,0xda,0xcd,0xc4,0xcc,0xd4,0xdc}
def jumps_into(r,offset,length):
    """(source file offset, target cpu addr) for every jr/jp/call that lands strictly inside the range"""
    bank=offset//0x4000;lo=offset if bank==0 else 0x4000+offset%0x4000;hi=lo+length;hits=[]
    banks=range(64) if bank==0 else [bank,0]
    for b in banks:
        s=b*0x4000
        for i in range(s,s+0x4000-2):
            op=r[i];cpu=i if b==0 else 0x4000+i%0x4000
            if op in JR and (b==bank or bank==0 and b==0):
                d=r[i+1];t=cpu+2+(d-256 if d>127 else d)
                if lo<t<hi:hits.append((i,t))
            elif op in JPC:
                t=r[i+1]|r[i+2]<<8
                if lo<t<hi and (bank==0 or t>=0x4000):hits.append((i,t))
    return hits

def check_hook(rom_before,rom_after,offset,length,provides=(),allow_jumps_from=(),max_steps=400):
    """Check a hook patch. rom_before = ROM without this patch, rom_after = ROM with it (stub code present).
    The patch must start with call/jp to the stub. Returns a list of problem strings (empty = OK)."""
    probs=[];bank=offset//0x4000;cpu=offset if bank==0 else 0x4000+offset%0x4000
    for src,t in jumps_into(rom_before,offset,length):
        if src not in allow_jumps_from:probs.append('jump from file $%05x lands inside the patch at $%04x'%(src,t))
    first=rom_after[offset]
    if first not in (0xcd,0xc3):return probs
    stub=rom_after[offset+1]|rom_after[offset+2]<<8
    A_old=Analyzer(rom_before,max_steps);A_new=Analyzer(rom_after,max_steps)
    # registers the original code reads after the patched bytes, not set by the replaced instructions themselves
    # registers the original code reads after the hook: a short horizon (real dependencies are immediate; a long
    # search drifts into data tables and reports noise)
    after=Analyzer(rom_before,max_steps=80,max_depth=2).live_in(bank,cpu+length)
    replaced_writes=set();a=cpu;watch={};kc={}
    while a<cpu+length:
        ins=decode(rom_before,bank,a)
        if ins['kind']=='call' and ins['target']==PREDEF:replaced_writes|={'a','b','c','d','e','h','l','f'}
        if ins['op']==0x21:kc['hl']=ins['imm']
        if ins['op']==0x06:kc['b']=ins['imm']
        if ins['kind']=='call' and ins['target']==BANKSWITCH and 'hl' in kc and 'b' in kc:
            cw,_=A_old.may_write(kc['b'],kc['hl']);replaced_writes|=cw|{'a','b','f'}
        if ins['kind']=='call' and ins['target'] not in (None,BANKSWITCH,PREDEF):
            # the stub may legitimately set this callee's inputs the same way the replaced code did before it
            watch[ins['target']]=A_old.live_in(bank,ins['target'])-replaced_writes
            cw,_=A_old.may_write(bank,ins['target'])
            replaced_writes|=cw            # what the original call itself changed is not the stub's fault
        replaced_writes|=ins['writes']
        a+=ins['len']
    need=after-replaced_writes-set(expand(provides))
    if first==0xcd:
        changed,pr=A_new.may_write(bank,stub,watch=watch);probs+=pr
        bad=need&changed
        if bad:probs.append('stub $%04x leaves %s changed, but the code after the hook reads them'%(stub,sorted(bad)))
    else:
        _,pr=A_new.may_write(bank,stub,watch=watch);probs+=pr
    return probs
