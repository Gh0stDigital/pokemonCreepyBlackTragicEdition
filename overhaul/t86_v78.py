# v78: the climax. Modes:
#  evo   - the evolution scene loads the pictures RED (86), GHOST (1F), BLACK (7F) in turn (RED -> GHOST -> BLACK); the text and BLACK as before
#  alone - GHOST is the only party member (besides ?????): after the climax it is gone anyway (party = BLACK, PRETA, AZHI)
import sys
MY86=sys.argv[1]
sys.argv=['x','none']
exec(open('t35_v25.py').read().split("if MODE=='items':")[0])
def ok(c,msg):print(('PASS ' if c else 'FAIL ')+msg,flush=True)
pics=[]
p.hook_register(0x1e,0x7f04,lambda c:pics.append(m[0xd0b5]),None)
ritual_state();T(30)
if MY86=='alone':
    n=m[0xd163];sp=list(m[0xd164:0xd164+n]);print('party before',[hex(x) for x in sp])
    gi=sp.index(0x1f);mi=sp.index(MIR)
    st=[bytes(m[0xd16b+44*i:0xd16b+44*(i+1)]) for i in (gi,mi)]
    ot=[bytes(m[0xd273+11*i:0xd273+11*(i+1)]) for i in (gi,mi)]
    nk=[bytes(m[0xd2b5+11*i:0xd2b5+11*(i+1)]) for i in (gi,mi)]
    m[0xd163]=2;m[0xd164]=0x1f;m[0xd165]=MIR;m[0xd166]=0xff
    for j in range(2):
        m[0xd16b+44*j:0xd16b+44*(j+1)]=st[j];m[0xd273+11*j:0xd273+11*(j+1)]=ot[j];m[0xd2b5+11*j:0xd2b5+11*(j+1)]=nk[j]
    print('party now',[hex(x) for x in party()],flush=True)
p.button('down',8);T(24);p.button('down',8);T(30)
for k in range(600):
    T(1)
    if MIR not in party():break
for k in range(40):
    if 'MIRAGE' in allt() and not box():break
    press_('a',45)
for k in range(2):
    press_a_until(lambda:not box(),n=10,wait=40)
    p.button('down',8);T(24)
for k in range(400):
    if m[0xd057]:break
    p.tick()
ok(m[0xd057]==1 and m[RIT]==5,'the GHOST battle starts')
seen.clear();pics.clear();texts=[];shots=[]
for k in range(9000):
    p.tick();b=clean(box())
    if b and (not texts or texts[-1]!=b):texts.append(b)
    if m[0xd057]==0 and k>300:break
    if k%40==20:p.button('a',8)
    if k>450 and k%16==0 and m[0xff47]!=0xff and len(shots)<60:shots.append(p.screen.image.copy().convert('RGB'))
T(300)
from PIL import Image
if shots:
    W,H=shots[0].size;sh=Image.new('RGB',(W*10,H*((len(shots)+9)//10)))
    for i,im in enumerate(shots):sh.paste(im,((i%10)*W,(i//10)*H))
    sh.save('qa/v78_evo_sheet.png')
print('pictures loaded by the evolution:',[hex(x) for x in pics],flush=True)
seq=[x for i,x in enumerate(pics) if i==0 or pics[i-1]!=x]
ok(0x86 in pics and 0x1f in pics and 0x7f in pics and pics.index(0x86)<pics.index(0x1f)<len(pics)-1-pics[::-1].index(0x7f) if 0x7f in pics else False,'the scene shows RED, then GHOST, then BLACK')
full=' '.join(texts)
ok('transcended' in full and 'You are now' in full,'"GHOST has transcended and become BLACK." / "You are now BLACK." as before')
print('party after',[hex(x) for x in party()],flush=True)
ok(m[0xd46c]==1 and m[RIT]==6 and 0x1f not in party() and party()[0]==0x7f,'BLACK is born and GHOST is not in the party')
print('t86 done',flush=True)
