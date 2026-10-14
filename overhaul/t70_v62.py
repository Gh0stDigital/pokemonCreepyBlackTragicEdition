# v62: CERULEAN CAVE: PROF. OAK. Modes:
#  scene  - BLACK, D876 = 6: OAK stands where MEWTWO waits; talking plays the white-screen scene (no music), his speech, then the battle
#           (name PROF.OAK, his picture, the six POKeMON, forbidden moves refused with his line); BANE kills him; D876 = 7, the end starts
#  normal - not BLACK / D876 < 6: MEWTWO is as before
import sys
MY70=sys.argv[1]
sys.argv=['x','none'];exec(open('t52_v44.py').read().split("if MODE=='block':")[0]);MODE=MY70
def setup():
    make_black();lead(CHAR);strong(0)
    b=0xd16b+44;m[b+9]=0x0a;m[b+30]=35
    m[0xd867]|=2;m[0xd876]=6
def to_oak():
    pass                                              # MEWTWO's spot is across the water (SURF): the scene is requested by hand (what his text does)
if MODE=='scene':
    warp(0xe3,0,setup)
    to_oak()
    print('at',pos(),'objects',[(i,hex(m[0xc100+16*i]),m[0xc204+16*i]-4,m[0xc205+16*i]-4) for i in range(1,4)],flush=True)
    ok(m[0xc110]==3,'object 1 is OAK (picture 3)')
    shot('v70_oak_cave')
    m[0xd877]=0x10;seen.clear()
    mus=[]
    for i in range(30):
        T(10)
        if i==6:shot('v70_scene');mus.append(m[0xcfca])
        if box():shot('v70_scene2');break
    print('scene: pic?','last music',hex(m[0xcfca]),flush=True)
    t=allt().replace('  ',' ')
    for i in range(300):
        if m[0xd057] or m[0xd877]==0x11:break
        if box():press_('a',80)
        else:T(20)
    t=allt().replace('  ',' ');print('speech:',t[-300:],flush=True)
    keys=['found me','BILL would buy me','Forgive me','mistakes','I was a fool','ambitions of that clan','gave the LEAGUE','mountain goddess','ocean god','BLUE must have failed',"MEWTWO",'one chance left','sorry','make things right','fix everything']
    print([k for k in keys if k not in t.replace("'","")])

    ok(all(k in t.replace("'","") for k in keys),"OAK's speech")
    for i in range(60):
        if m[0xd057] and m[0xd89c]:break
        press_('a',100)
    T(100)
    n=m[0xd89c];sp=list(m[0xd89d:0xd89d+n])
    from patchlib import enc
    print('battle',m[0xd057],'class',m[0xd031],'party',[hex(x) for x in sp],'pic',hex(m[0xd033]|m[0xd034]<<8),bytes(m[0xd04a:0xd04a+9]).hex(),flush=True)
    ok(m[0xd057]==2 and m[0xd031]==26,'a trainer battle (class 26)')
    ok(sp==[0x2a,0x9a,0x4a,0x4b,0x49,0x15],'MR. MIME, VENUSAUR, ARTICUNO, ZAPDOS, MOLTRES, MEW (last)')
    ok((m[0xd033]|m[0xd034]<<8)==0x615f and bytes(m[0xd04a:0xd04a+9])==bytes(enc('PROF.OAK'))+b'\x50',"his picture and the name PROF.OAK")
    shot('v70_oak_battle')
    m[0xd89c]=1;wait_menu()
    menu('fight');m[0xcc26]=1;T(4);seen.clear();p.button('a',8)
    for k in range(2500):
        p.tick()
        if k%4==0:T(1)
        if m[0xd05a]==3 and 'FIGHT' in clean(' '.join(txt())):break
        if k%90==0:p.button('a',8)
    tt=allt().replace('  ',' ');print('to phase:',tt[-300:],flush=True)
    ok('shatters' not in tt,'no MOON STONE shatter text for him')
    keys=['couldnt prevent','Forgive me','fool all along','How foolish','Pandora','unleash']
    print([k for k in keys if k not in tt.replace("'","")])
    ok(all(k in tt.replace("'","") for k in keys),'his defeat speech')
    seen.clear();use_move(0,300,in_moves=True)
    for i in range(30):
        if m[0xd057]==0:break
        press_('a',100)
    ok(m[0xd057]==0,'the battle is over (BANE)')
    T(60)
    print('stage',m[0xd876],'music',hex(m[0xcfca]),hex(m[0xd35b]),flush=True)
    ok(m[0xd876]==7,'D876 = 7: the end')
elif MODE=='block':                                  # BLACK leads: BANE is refused with his line
    def setup3():
        make_black();m[0xd16b+29]=20
        m[0xd867]|=2;m[0xd876]=6
    warp(0xe3,0,setup3)
    m[0xd877]=0x10
    for i in range(300):
        if m[0xd877]==0x11 or m[0xd057]:break
        if box():press_('a',60)
        else:T(15)
    for i in range(60):
        if m[0xd057] and m[0xd89c]:break
        press_('a',100)
    T(100);m[0xd89c]=1;wait_menu()
    ok(m[0xd031]==26 and m[0xd014]==BLK,'OAK fights BLACK')
    e0,p0=ehp(),php()
    lo=use_move(0,300);read_until_menu();t=allt().replace('  ',' ');print('forbidden:',t[-300:],flush=True)
    ok('strange power' in t and 'I was right' in t and 'MOON STONES' in t,'a forbidden move is refused with his line')
    ok(m[0xd057]==2 and ehp()==e0 and php()==p0,'no turn passed')
