# Round-trip check for sm83asm.py: disassemble real code from the ROM (ref/dis.py), re-assemble it, compare bytes.
import re,subprocess,sys
from sm83asm import asm
ROM='overhaul/Creepy_Black_Mu_v24.gb'
REGIONS=[(3,0x58f8,40),(0xf,0x6d78,22),(0xf,0x52bf,22),(0,0x1077,26),(0xe,0x7e34,40),(0x2e,0x4300,60),(0xf,0x5629,40),(0,0x3618,14),(0x1e,0x7f21,24),(0x1c,0x52b3,44),(0x1c,0x5927,18)]
bad=0
for bank,addr,n in REGIONS:
    out=subprocess.run([sys.executable,'ref/dis.py',ROM,hex(bank),hex(addr),str(n)],capture_output=True,text=True,cwd='..').stdout
    lines=[];raw=bytearray()
    for l in out.splitlines():
        m=re.match(r'^[0-9a-f]{2}:([0-9a-f]{4})\s+((?:[0-9a-f]{2} )+)\s*(.*?)(?:\s+;.*)?$',l)
        if not m:continue
        b=bytes.fromhex(m.group(2).replace(' ',''));ins=m.group(3).strip()
        if ins.startswith('db '):continue
        lines.append(ins);raw+=b
    assert raw,('no instructions parsed',hex(bank),hex(addr),out[:200])
    base=addr
    try:code,_=asm('\n'.join(lines),base)
    except Exception as e:print('FAIL',hex(bank),hex(addr),e);bad+=1;continue
    if code!=bytes(raw):
        i=next(k for k in range(min(len(code),len(raw))) if code[k]!=raw[k]) if code[:len(raw)]!=raw[:len(code)] else min(len(code),len(raw))
        print('MISMATCH',hex(bank),hex(addr),'at +',i,code[i:i+4].hex(),raw[i:i+4].hex());bad+=1
    else:print('ok',hex(bank),hex(addr),len(raw),'bytes')
sys.exit(1 if bad else 0)
