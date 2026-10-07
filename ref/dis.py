# Tiny GB disassembler: python ref/dis.py ROM BANK ADDR [N]
import sys,re
sys.path.insert(0,'ref');from instruction_set import instructions,cb_instructions
ram={}
for l in open('ref/pokered.sym'):
    m=re.match(r'([0-9a-f]{2}):([0-9a-f]{4}) (\S+)',l)
    if m:
        a=int(m.group(2),16)
        if a>=0xc000 and '.' not in m.group(3):ram.setdefault(a,m.group(3))
def dis(r,bank,addr,n=40,out=None):
    o=addr if addr<0x4000 else bank*0x4000+addr-0x4000
    lines=[]
    for _ in range(n):
        op=r[o];a=addr
        if op==0xcb:t=cb_instructions[r[o+1]];ln=2
        else:
            t=instructions.get(op,'db $%02x'%op);ln=1
            if 'd16' in t or 'a16' in t:
                v=r[o+1]|r[o+2]<<8;nm=ram.get(v,'');t=t.replace('d16','$%04x'%v).replace('a16','$%04x'%v)+('  ; '+nm if nm else '');ln=3
            elif 'pc+r8' in t:
                d=r[o+1];d=d-256 if d>127 else d;t=t.replace('pc+r8','$%04x'%(addr+2+d));ln=2
            elif 'd8' in t or 'a8' in t or 'r8' in t:
                v=r[o+1];t=t.replace('d8','$%02x'%v).replace('a8','$%02x'%v).replace('r8','$%02x'%v)
                if 'ff00' in t or "ldh" in t: nm=ram.get(0xff00+v,'');t+=('  ; '+nm if nm else '')
                ln=2
        lines.append('%02x:%04x  %-12s %s'%(bank,a,r[o:o+ln].hex(' '),t))
        o+=ln;addr+=ln
    return '\n'.join(lines)
if __name__=='__main__':
    r=open(sys.argv[1],'rb').read();print(dis(r,int(sys.argv[2],16),int(sys.argv[3],16),int(sys.argv[4]) if len(sys.argv)>4 else 40))
