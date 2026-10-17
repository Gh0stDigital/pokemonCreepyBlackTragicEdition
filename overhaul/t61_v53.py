# v53: Tower 7F channelers, the door after AGATHA's talk, the altar stash. Modes:
#  lore    - stage 5 (consort arrived): ten channelers (picture 19) stand in the hall, five on each side; each tells its part
#            (titles checked); stage 4 and the finished ritual (RIT 6): none
#  door    - stage 5 without the door flags: stairs closed, AGATHA in front; her talk sets the flag, she walks up and left, the
#            stairs open; the stairs lead to the chamber; coming back: open, AGATHA beside; stage 4: closed as always
#  ritualstash - the climax with PRETA in the stash: it is back once afterwards
#  altar   - chamber with PRETA and AZHI in the party (awakened by MR. MU): they leave the party, the stands play the cry and say
#            "stands still", the helix stand is plain; leaving puts them back; not awakened: plain texts; RIT 3: the fossil
#            sprites are gone and nothing is stashed
import sys,json
MY61=sys.argv[1]
sys.argv=['x','none'];exec(open('t34_v23.py').read().split("if MODE in ('ritual','no','partyfull'):")[0]);MODE=MY61
def ok(c,msg):
    print(('PASS ' if c else 'FAIL ')+msg,flush=True)
    if not c:sys.exit(1)
def box():                                  # only a drawn text box counts (the hall's wall tiles read as letters)
    if m[0xc3a0+12*20]!=0x79:return ''
    return ' | '.join(x for x in txt()[12:] if x)
def fo(b,a):return b*0x4000+a-0x4000
from patchlib import enc
MAN=json.load(open('manifest_v53.json'));SPOTS=MAN['spots']
TITLES=['Ancient Clan','God of the','Division','Four Warriors','Eight Dragons','Forbidden Art','Sacred Grounds','Ancient Trials','Lavender Cult','Forgotten God']
def sprites():return {i:(m[0xc100+16*i],m[0xc204+16*i]-4,m[0xc205+16*i]-4,m[0xd4e4+2*(i-1)+1]) for i in range(1,16) if m[0xc100+16*i] and m[0xc204+16*i]!=0xff}
def chs():return {i:v for i,v in sprites().items() if v[0]==0x19}
def tower53(stage=5,consort=1,bits=0x00,rit=0):
    load('pallet_with_ghost');m[0xd455]=255
    m[0xd769]|=0x8e;m[0xd7e0]|=0x80;m[0xd5ae]|=0x0f;m[0xd464]=stage;m[0xd465]=consort;m[0xd466]=bits;m[0xd467]=rit
    for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=0;m[0xd3af+4*i+3]=0x94
    for i in range(6):
        if m[0xd35e]==0x94:break
        p.button('up',8);T(24)
    T(120);m[0xd887]=0
def block_at(by,bx):return m[0xc6e8+(by+3)*(m[0xd369]+6)+bx+3]
def talk_at(y,x,face,n=30):
    bfs_to(y,x);p.button(face,8);T(30);seen.clear();press_('a',50)
    for k in range(n):
        if not box():
            T(40)
            if not box():break
        press_('a',60)
    return allt()
if MODE=='lore':
    tower53(5)
    ok(len(chs())==0,'at the entrance (row 16) none is drawn yet: only channelers within two steps of the player are shown (the GB draws ten sprites)')
    seen_spots=set();most=0;got=[]
    for k,(y,x,f,t) in enumerate(SPOTS):
        sx,face=(10,'left') if x==9 else (11,'right')
        txt_=talk_at(y,sx,face);c=chs();most=max(most,len(c));seen_spots|={(v[1],v[2]) for v in c.values()}
        print(k+1,'visible now',len(c),txt_[:60])
        for b in range(8):
            if box():press_('a',60)
        ok('SHAMANESS' in txt_ and ('SHAMANESS %d'%(k+1)) in txt_.replace('  ',' '),'Shamaness %d at (%d,%d) tells "%s"'%(k+1,y,x,TITLES[k]))
    want={(y,x) for y,x,f,t in SPOTS}
    ok(seen_spots==want,'all ten spots were seen, five on each side (x 9 and x 12, rows 4..12)')
    ok(most<=6,'never more than six channelers drawn at once (%d)'%most)
    tower53(4)
    ok(len(chs())==0,'stage 4: no channelers')
    tower53(5,rit=6)
    ok(len(chs())==0,'ritual done (RIT 6): no channelers')
elif MODE=='door':
    tower53(4,bits=0)
    ok(block_at(0,5)!=0x11 and m[0xc150]==0x39,'stage 4: door closed, AGATHA in front (picture 39)')
    tower53(5,bits=0)
    ay,ax=m[0xc254]-4,m[0xc255]-4;print('AGATHA',ay,ax,'block',hex(block_at(0,5)))
    ok(m[0xc150]==0x39 and (ay,ax)==(3,11) and block_at(0,5)!=0x11,'stage 5: AGATHA stands in front, the door is closed')
    t=talk_at(4,11,'up',n=20);print(t)
    for k in range(40):
        if m[0xd466]&0x10:break
        press_('a',30) if box() else T(30)
    for k in range(10):T(30)
    ay,ax=m[0xc254]-4,m[0xc255]-4;print('after talk: AGATHA',ay,ax,'flags',hex(m[0xd466]),'block',hex(block_at(0,5)))
    ok('open now' in t.replace('  ',' ') and m[0xd466]&0x18==0x18,'AGATHA: "the ritual room is open now" - flags set')
    ok((ay,ax)==(2,10) and block_at(0,5)==0x11,'she stepped up and left; the graves are the stairway')
    bfs_to(2,11);p.button('up',16);T(200);ok(pos()[0]==0x69,'the stairs lead into the chamber %s'%str(pos()))
    tower53(5,bits=0x18)
    ay,ax=m[0xc254]-4,m[0xc255]-4
    ok((ay,ax)==(2,10) and block_at(0,5)==0x11,'coming back: door open, AGATHA beside it')
    t=talk_at(2,11,'left',n=15);print(t[-100:])
    ok('ritual room is' in t.replace('  ',' ') or 'Go when' in t,'her later talk: the room is open')
elif MODE=='altar':
    PS=fo(0x2e,0x469a);ROMB=open(os.environ['CB_ROM'],'rb').read()
    SA=fo(0x2d,int(json.load(open('manifest_v52.json'))['labels']['bank2d']['s_azhi35'],16))
    def add(struct,name):
        n=m[0xd163];m[0xd164+n]=struct[0];m[0xd164+n+1]=0xff;m[0xd163]=n+1
        m[0xd16b+44*n:0xd16b+44*n+44]=list(struct);m[0xd2b5+11*n:0xd2b5+11*n+11]=list(enc(name))+[0x50]*(11-len(name))
    def enter(mu2=2,rit=0):
        tower53(5,bits=0x18,rit=rit);m[0xd460]=mu2
        add(ROMB[PS:PS+44],'PRETA');add(ROMB[SA:SA+44],'AZHI')
        bfs_to(2,11);p.button('up',16);T(200);T(60)
    cries=[];p.hook_register(0,0x13ff,lambda c:cries.append(p.register_file.A),None)
    enter(2)
    ok(pos()[0]==0x69,'in the chamber')
    pt=list(m[0xd164:0xd164+m[0xd163]]);print('party in chamber',[hex(x) for x in pt],'flags',hex(m[0xd466]))
    ok(0xb6 not in pt and 0xb7 not in pt and m[0xd466]&0x40,'PRETA and AZHI left the party (stashed)')
    print('sprites',sprites())
    ok(all(i in sprites() for i in (2,3,4)),'the three fossil sprites are on the stands')
    cries.clear();t=talk_at(15,7,'left',n=10);print('DOME stand:',t[-90:],cries)
    ok('PRETA' in t and 'still' in t and 0xb6 in cries,'DOME stand (PRETA awakened): its cry and "PRETA stands still on the stand."')
    AMB=(15,15,'right') if VERSION>=76 else (8,11,'up')        # v76: AMBER on the right stand, HELIX on the top one
    HEL=(8,11,'up') if VERSION>=76 else (15,15,'right')
    m[0xd460]=4;cries.clear();t=talk_at(*AMB,n=10);print('AMBER stand:',t[-90:],cries)
    ok('AZHI' in t and 'still' in t and 0xb7 in cries,'AMBER stand (AZHI awakened): its cry and "AZHI stands still on the stand."')
    cries.clear();t=talk_at(*HEL,n=10);print('HELIX stand:',t[-90:])
    ok('HELIX FOSSIL' in t and not cries,'HELIX stand: plain text, no cry')
    bfs_to(18,11);p.button('down',16);T(200);T(60)
    pt=list(m[0xd164:0xd164+m[0xd163]]);print('back on 7F',pos(),[hex(x) for x in pt],hex(m[0xd466]))
    ok(pos()[0]==0x94 and pt.count(0xb6)==1 and pt.count(0xb7)==1 and not m[0xd466]&0x40,'leaving: PRETA and AZHI are back in the party')
    b=0xd16b+44*pt.index(0xb6);ok(m[b+33]==25 and (m[b+1]<<8|m[b+2])>0,'PRETA is as it was (Lv25, HP)')
    enter(0);t=talk_at(15,7,'left',n=10);print('plain:',t[-80:])
    ok('DOME FOSSIL' in t and 'stands still' not in t,'not awakened (D460 0): the stand says it rests there')
    enter(2,rit=3);pt=list(m[0xd164:0xd164+m[0xd163]])
    ok(0xb6 in pt and not m[0xd466]&0x40 and not any(i in sprites() for i in (2,3,4)),'after the ritual (RIT 3): nothing stashed, the fossil sprites are gone')
elif MODE=='ritualstash':                               # PRETA waits in the stash while the ritual ends: it comes back first, black_join gives no second PRETA
    PS=fo(0x2e,0x469a);ROMB=open(os.environ['CB_ROM'],'rb').read()
    exec(open('t46_v38.py').read().split("if MODE in ('join','owned'):")[0].split("def climax")[1].join(["def climax",""]) if False else "")
    src=open('t46_v38.py').read();a=src.index("def climax");b=src.index("if MODE in ('join','owned'):")
    exec(src[a:b])
    def s():
        m[0xd466]|=0x40
        st=bytes(ROMB[PS:PS+44])+bytes(enc('PRETA'))+bytes([0x50]*6)+bytes(11)
        m[1,0xba00]=1
        for i,v in enumerate(st):m[1,0xba01+i]=v
        n=m[0xd163]
        print('party before',[hex(x) for x in m[0xd164:0xd164+n]])
    climax('v25_after_ritual_v25a',s)
    pt=list(m[0xd164:0xd164+m[0xd163]]);print('party after',[hex(x) for x in pt],'flags',hex(m[0xd466]),'box',m[0xda80])
    ok(pt.count(0xb6)==1 and not m[0xd466]&0x40,'the stashed PRETA is back (once, not given twice by black_join), the stash flag is clear')
    ok(0x7f in pt,'BLACK joined as before')
