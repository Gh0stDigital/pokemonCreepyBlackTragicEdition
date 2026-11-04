# v61: BILL's team (FLAREON, VAPOREON, JOLTEON, CHANSEY, ALAKAZAM, PORYGON last) and the PSYCHIC trainer picture
import sys
sys.argv=['x','none'];exec(open('t52_v44.py').read().split("if MODE=='block':")[0])
def setup():
    make_black();lead(CHAR);strong(0)
    m[0xd867]|=2;m[0xd876]=5
warp(0x58,0,setup)
for i in range(80):
    if m[0xd057]:break
    if box():press_('a',80)
    else:T(20)
T(200)
n=m[0xd89c];sp=list(m[0xd89d:0xd89d+n]);lv=[m[0xd8a8+44*i+33] if False else 0 for i in range(n)]
print('enemy party',n,[hex(x) for x in sp],'class',m[0xd031],'pic ptr',hex(m[0xd033]|m[0xd034]<<8),flush=True)
ok(m[0xd031]==26,'BILL (class 26)')
RB=open(ROM,'rb').read() if isinstance(ROM,str) else bytes(ROM)
def spname(x):return ''.join({0x85:'F',0x8b:'L',0x80:'A',0x91:'R',0x84:'E',0x8e:'O',0x8d:'N',0x95:'V',0x8f:'P',0x89:'J',0x93:'T',0x82:'C',0x87:'H',0x92:'S',0x98:'Y',0x8a:'K',0x99:'Z',0x8c:'M',0x86:'G',0x94:'U',0x83:'D',0x81:'B',0x88:'I',0x96:'W',0x97:'X',0x90:'Q',0xe8:'.'}.get(b,'?') for b in RB[0x1c21e+10*(x-1):0x1c21e+10*x] if b!=0x50)
names=[spname(x) for x in sp];print('names',names,flush=True)
if VERSION>=102:ok(names==['FLAREON','VAPOREON','JOLTEON','CHANSEY','ALAKAZAM','PORYGON'],'FLAREON, VAPOREON, JOLTEON, CHANSEY, ALAKAZAM, PORYGON (last), by the game\'s own names')
else:ok(sp==[0x6a,0x69,0x68,0x28,0x95,0xaa],'v61 bytes (slot 1 = $6A = MACHOP, fixed in v102)')
ok((m[0xd033]|m[0xd034]<<8)==0x5728,"the PSYCHIC trainer's picture")
shot('v61_bill_pic')
