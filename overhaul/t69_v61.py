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
ok(sp==[0x6a,0x69,0x68,0x28,0x95,0xaa],'FLAREON, VAPOREON, JOLTEON, CHANSEY, ALAKAZAM, PORYGON (last)')
ok((m[0xd033]|m[0xd034]<<8)==0x5728,"the PSYCHIC trainer's picture")
shot('v61_bill_pic')
