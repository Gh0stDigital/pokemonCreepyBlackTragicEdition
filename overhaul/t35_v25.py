# v25 climax after MR. MU's ritual. Modes (all start from a ritual-complete chamber state that is built once per ROM):
#  items    - every item refused in the chamber (text, bag unchanged); Dig/Teleport/Fly refused
#  icon     - party menu: ????? has the hollow-gentleman icon tiles (2C/2E, frame 2 6C/6E), GHOST keeps its own
#  climax   - walk out of the circle -> GHOST consumes the MIRAGE; two steps later the GHOST battle; CURSE, black screen,
#             evolution, BLACK (name, flag, party without GHOST/?????); saves v25_black
#  sprites  - BLACK: map sprite sheet in VRAM and the battle back picture
#  agatha   - back on Tower 7F AGATHA walks up and talks; two more talks
#  house    - the consort waits in the player's house 1F and heals; hidden before the ritual
#  normal   - normal cases: items work outside the chamber, hunger runs unless BLACK
import sys,io,os,hashlib
RUN=sys.argv[1]
sys.argv=['x','none']
exec(open('t34_v23.py').read().split("if MODE in ('ritual'")[0])        # shared helpers (bfs_to, chamber, talk_mu, ...)
MODE=RUN
ROM_BYTES=open(ROM,'rb').read()
ROMTAG='v25a'                      # cached states: delete qa/*v25a* when the chamber/7F code layout changes
import hollow_icon as ICON_MOD
ICON_TILES=ICON_MOD.four_tiles(open(ROM,'rb').read())
def state_exists(n):return (qa/(n+'.state')).exists()
def ritual_state():
    """chamber, ritual finished (RIT=3), ????? in the party; cached per ROM build"""
    name='v25_after_ritual_'+ROMTAG
    if state_exists(name):load(name);T(30);return
    chamber();set_bag([(POTION,3)])
    talk_mu('yes');assert wait_menu(),'no battle menu'
    for k in range(60):
        if m[0xcfe5]==MIR:break
        if menu_shown():choose('FIGHT');press_('a',60)
        else:press_('a',60)
    for k in range(10):
        if menu_shown():break
        press_('a',60)
    choose('ITEM');T(30);pick_item('MASTER');press_('a',10)
    for k in range(3000):
        p.tick()
        if k%120==0:p.button('a',8)
        if not m[0xd057] and k>200:break
    T(400);assert m[RIT]==3 and party()[-1]==MIR,(m[RIT],party())
    save(name)
def press_a_until(cond,n=40,key='a',wait=60):
    for k in range(n):
        if cond():return True
        press_(key,wait)
    return cond()
def start_select(name):
    """open the START menu and choose an entry by name (the cursor remembers its last position)"""
    p.button('start',8);T(40)
    for k in range(8):
        row=[l for l in txt() if '▶' in l or '▲' in l]
        if row and name in row[0]:break
        press_('down',20)
    press_('a',60)
def open_party():start_select('POK')
def close_menus():
    for k in range(8):press_('b',25)

if MODE=='items':
    ritual_state();b0=bag();print('party',[hex(x) for x in party()],'bag',b0)
    set_bag([(POTION,3),(0x1d,1)]);b0=bag()              # POTION, ESCAPE ROPE
    for item,idx in (('POTION',0),('ESCAPE',1)):
        start_select('ITEM')
        for k in range(idx):press_('down',20)
        seen.clear();press_('a',50);press_('a',60)                       # item, USE
        for k in range(4):
            if 'prevents' in allt():break
            press_('a',60)
        print(item,'->',allt()[-80:])
        assert 'prevents' in allt() and 'Use on' not in allt() and bag()==b0,(item,allt(),bag())
        close_menus()
        assert not box(),box()
    print('PASS every item is refused in the chamber (POTION, ESCAPE ROPE): bag unchanged',flush=True)
    DIG,TELE,FLY=0x5b,0x64,0x13
    m[0xd16b+8:0xd16b+12]=bytes([DIG,TELE,FLY,0])
    for name,idx in (('DIG',0),('TELEPORT',1),('FLY',2)):
        open_party();press_('a',60)                                       # first mon -> submenu
        s=scr();print(name,'submenu:',s[-120:])
        for k in range(idx):press_('down',20)
        seen.clear();press_('a',60)
        for k in range(4):
            if 'prevents' in allt():break
            press_('a',60)
        assert 'prevents' in allt(),(name,allt(),scr())
        close_menus()
    print('PASS Dig / Teleport / Fly are refused in the chamber',flush=True)
elif MODE=='icon':
    ritual_state();open_party();T(60)
    tiles=set()
    for k in range(120):
        p.tick()
        for i in range(40):
            if m[0xfe00+4*i]:tiles.add(m[0xfe02+4*i])
    print('sprite tiles in the party menu',sorted(hex(t) for t in tiles))
    exp=ICON_TILES
    got=[bytes(m[a:a+16]) for a in (0x82c0,0x82e0,0x86c0,0x86e0)]
    print('VRAM matches',[g==e for g,e in zip(got,exp)])
    p.screen.image.save(S+'v25_party_icons.png')
    assert 0x2c in tiles or 0x6c in tiles,'no hollow icon sprite'
    assert 0x28 in tiles or 0x68 in tiles,'GHOST icon missing'
    assert got==exp,'icon tiles not in VRAM'
    print('PASS party menu: ????? uses the hollow gentleman icon tiles, GHOST keeps its own',flush=True)
elif MODE=='iconzoom':
    from PIL import Image
    ritual_state();open_party();T(40)
    shots=[]
    for sel in (0,1,2):
        for k in range(sel and 1):press_('down',20)
        for ph in range(2):
            T(14);im=p.screen.image.copy().convert('RGB').crop((0,0,40,56));shots.append(im.resize((40*6,56*6),Image.NEAREST))
    W=sum(i.width for i in shots)+10*len(shots);c=Image.new('RGB',(W,shots[0].height),'white');x=0
    for i in shots:c.paste(i,(x,0));x+=i.width+10
    c.save(S+'v25_icon_zoom.png')
elif MODE=='climax':
    from PIL import Image
    ritual_state();p0=party();print('party',[hex(x) for x in p0],pos(),'RIT',m[RIT],flush=True)
    assert pos()==(0x69,11,12) and m[RIT]==3 and p0==[0xb0,0x1f,MIR],(pos(),m[RIT],p0)
    seen.clear()
    p.button('down',8);T(24);print('inside the circle',pos(),'RIT',m[RIT]);assert m[RIT]==3 and m[0xd46c]==0
    p.button('down',8);T(30);print('first step outside',pos(),'RIT',m[RIT],flush=True)
    for k in range(600):                                  # cry + flash are still playing
        T(1)
        if MIR not in party():break
    print('????? left the party after',k,'frames')
    for k in range(40):
        if 'MIRAGE' in allt() and not box():break
        press_('a',45)
    print('consume text:',allt()[-120:],'party',[hex(x) for x in party()])
    assert m[RIT]==4 and party()==[0xb0,0x1f] and 'consumed' in allt() and 'MIRAGE' in allt()
    print('PASS the first step out of the circle: GHOST consumed the MIRAGE (????? left the party), 2 steps to go',flush=True)
    p.screen.image.save(S+'v25_consumed.png')
    for k in range(2):
        press_a_until(lambda:not box(),n=10,wait=40)
        p.button('down',8);T(24)
        print('step',k+1,pos(),'STEPS',m[0xd46a],'RIT',m[RIT],flush=True)
    assert m[0xd46a]==2 or m[RIT]==5,(m[0xd46a],m[RIT])
    for k in range(400):
        if m[0xd057]:break
        p.tick()
    assert m[0xd057]==1 and m[RIT]==5 and m[0xcfe5]==0x1f and m[0xcff3]==100,(m[0xd057],m[RIT],hex(m[0xcfe5]),m[0xcff3])
    print('PASS two steps later the battle starts: wild GHOST Lv%d vs the player (YOU) alone, party %s'%(m[0xcff3],[hex(x) for x in party()]),flush=True)
    seen.clear();runs=[];run=0;shots=[];last_bgp=None;t_start=None;ev_seen=False;texts=[];done_shots=set()
    for k in range(9000):
        p.tick();bgp=m[0xff47]
        b=clean(box())
        if b and (not texts or texts[-1]!=b):texts.append(b)
        if m[0xd057]==0 and k>300:break
        for key,fn in (('transcended','v25_trans.png'),('You are now','v25_now.png')):
            if key in b and fn not in done_shots:done_shots.add(fn);p.screen.image.save(S+fn)
        if bgp==0xff and m[0xd057]:run+=1
        elif run:runs.append((k,run));run=0
        if k%10==0 and bgp!=0xff and k>450 and len(shots)<48:shots.append((k,bgp,p.screen.image.copy().convert('RGB')))
        if k%50==25:p.button('a',8)
    print('black runs (frame end, length):',runs)
    print('texts:',[t for t in texts if len(t)>14][:14])
    longest=max([r for _,r in runs] or [0])
    assert 'CURSE' in ' '.join(texts) and 'transcended' in ' '.join(texts) and 'BLACK' in ' '.join(texts)
    assert longest>=270,longest
    print('PASS CURSE first, then the screen stays black for %d frames (%.1f s), the evolution text follows'%(longest,longest/60),flush=True)
    sheet=Image.new('RGB',(8*164,((len(shots)+7)//8)*148),'white')
    for i,(k,bgp,im) in enumerate(shots):sheet.paste(im,((i%8)*164,(i//8)*148))
    sheet.save(S+'v25_climax_sheet.png')
    T(300)
    print('after: pos',pos(),'RIT',m[RIT],'BLACK',m[0xd46c],'name',''.join(cm.get(v,'') for v in m[0xd158:0xd163]),'party',[hex(x) for x in party()],'D057',m[0xd057],'D059',m[0xd059])
    assert m[0xd46c]==1 and m[RIT]==6 and party()==[0xb0] and m[0xd057]==0
    assert ''.join(cm.get(v,'') for v in m[0xd158:0xd15d])=='BLACK'
    p.screen.image.save(S+'v25_after_climax.png');save('v25_black_'+ROMTAG)
    print('PASS the player is BLACK (name, flag), GHOST and ????? left the party, the battle is over',flush=True)
def warp(mapid,warpid=0,setup=None):
    load('pallet_with_ghost');m[0xd455]=255
    if setup:setup()
    for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=warpid;m[0xd3af+4*i+3]=mapid
    for i in range(6):
        if m[0xd35e]==mapid:break
        p.button('up',8);T(24)
    T(120);print('arrived',hex(mapid),pos(),flush=True)
def dark_ratio(im,box):
    c=im.convert('L').crop(box);px=list(c.getdata());return sum(1 for v in px if v<60)/len(px)
if MODE=='sprites':
    from PIL import Image
    sheet=bytes(ROM_BYTES[0x2d*0x4000+0x7000-0x4000:0x2d*0x4000+0x7000-0x4000+0x180])
    load('v25_black_'+ROMTAG);T(60)
    v0=bytes(m[0x8000:0x80c0]);v1=bytes(m[0x8800:0x88c0])
    print('chamber VRAM sheet match:',v0==sheet[:0xc0],v1==sheet[0xc0:])
    assert v0==sheet[:0xc0] and v1==sheet[0xc0:]
    print('PASS BLACK map sprite sheet is in VRAM in the chamber',flush=True)
    res={}
    for tag,black in (('red',0),('black',1)):
        load('pallet_with_ghost');m[0xd455]=255;m[RIT]=6 if black else 0;m[0xd46c]=black
        m[0xd059]=0x24;m[0xd127]=5                                     # a wild PIDGEY
        im=None
        for k in range(1500):                      # the player's own back picture shows during the intro slide-in
            p.tick()
            b=clean(box())
            if m[0xd057] and 'appeared' in b and 'Go' not in b and im is None:
                T(10);im=p.screen.image.copy();im.save(S+'v25_back_%s.png'%tag)
            if im is not None and 'Go' in b:break
        assert im is not None,'no intro frame'
        assert wait_menu()
        res[tag]=dark_ratio(im,(0,40,80,104));print(tag,'back pic dark ratio',round(res[tag],2))
    assert res['black']>res['red']+0.05,res
    print('PASS the battle back picture is the blacked-out BLACK fusion when BLACK (RED otherwise)',flush=True)
    choose('RUN');press_('a',60)
    for k in range(40):
        if not m[0xd057]:break
        press_('a',60)
    T(120)
    v0=bytes(m[0x8000:0x80c0]);print('Pallet after the battle: sprite sheet match',v0==sheet[:0xc0])
    assert v0==sheet[:0xc0]
    im=p.screen.image.copy();im.save(S+'v25_pallet_black.png')
    print('PASS BLACK map sprite in Pallet Town after a battle',flush=True)
elif MODE=='agatha':
    load('v25_black_'+ROMTAG);T(30);print(pos())
    bfs_to(18,11);seen.clear();p.button('down',16)
    for k in range(3000):
        T(1)
        if m[0xd35e]==0x94 and m[0xd46f]==3 and not m[0xd730]&1 and not box():break
        if box() and k%50==20:p.button('a',8)
    print('arrived',pos(),'AGTALK',m[0xd46b],'SCENE',m[0xd46f],'joy',m[0xcd6b],'AGATHA',spr(9))
    t=allt();print(t[-200:])
    for key in ('It is','done','ceremony','consort','PALLET','work has','intruders','LEAGUE'):assert key in t,key
    assert m[0xd46b]==1 and spr(9)==('0x39',2,10) and m[0xcd6b]==0 and [spr(k)[0] for k in (6,7,8)]==['0x0']*3,(m[0xd46b],spr(9),[spr(k) for k in (6,7,8)])
    print('PASS AGATHA walked up, celebrated, told about the consort and the LEAGUE, then stepped back; the girls left 7F',flush=True)
    p.screen.image.save(S+'v25_agatha_scene.png')
    def talk_agatha():
        seen.clear()
        if pos()[2]!=2:p.button('down',8);T(24)
        p.button('left',8);T(30);press_('a',90)
        for k in range(40):
            if not box() and k>2:break
            press_('a',70)
        return allt()
    t2=talk_agatha();print('lore:',t2[-160:])
    assert 'MR. MU' in t2 and 'celebrate' in t2 and m[0xd46b]==2
    t3=talk_agatha();print('final:',t3[-160:])
    assert 'smiling' in t3 and 'outsiders' in t3 and m[0xd46b]==2
    t4=talk_agatha();assert 'smiling' in t4
    print('PASS AGATHA\'s talks: MR. MU\'s story, then the final line (repeats)',flush=True)
elif MODE=='house':
    for rit,consort,spr_id,name in ((3,1,None,'before the ritual'),(6,1,0x1d,'MISTY'),(6,2,0x1b,'ERIKA'),(6,3,0x0d,'SABRINA')):
        def setup(rit=rit,consort=consort):m[RIT]=rit;m[0xd465]=consort
        warp(0x25,0,setup)
        objs=[spr(k) for k in (1,2,3,4)];print(name,objs)
        if spr_id is None:
            assert [o[0] for o in objs[1:]]==['0x0']*3,objs
            print('PASS before the ritual nobody waits at home',flush=True);continue
        assert objs[0][0]=='0x33' and objs[[1,0x1d,0x1b,0x0d].index(spr_id) if False else 1+(consort-1)]==(hex(spr_id),5,6),objs
        assert [o[0] for i,o in enumerate(objs[1:]) if i!=consort-1]==['0x0']*2,objs
        print('PASS',name,'waits at home (5,6), the other two are hidden',flush=True)
    # talk + heal (SABRINA is loaded)
    m[0xd16c]=0;m[0xd16d]=3                                           # CHARMANDER HP = 3
    mx=m[0xd16b+34]<<8|m[0xd16b+35];print('max HP',mx,'HP',m[0xd16c]<<8|m[0xd16d])
    bfs_to(6,6);seen.clear();p.button('up',8);T(30)
    for k in range(40):
        press_('a',70)
        if not box() and k>2:break
    hp=m[0xd16c]<<8|m[0xd16d];print('talk:',allt()[-200:],'HP now',hp)
    assert 'SABRINA' in allt() and 'Rest' in allt() and 'better' in allt() and hp==mx
    print('PASS talking to her heals the party',flush=True)
elif MODE=='normal':
    set_bag([(POTION,3),(0x1d,1)])
    load('pallet_with_ghost');m[0xd455]=255;set_bag([(POTION,3)])
    m[0xd16c]=0;m[0xd16d]=5;mx=m[0xd16b+34]<<8|m[0xd16b+35]
    start_select('ITEM');seen.clear();press_('a',50);press_('a',60);press_('a',70)    # POTION, USE, first mon
    for k in range(6):press_('a',60)
    hp=m[0xd16c]<<8|m[0xd16d];print('potion outside the chamber: HP 5 ->',hp,'bag',bag())
    assert hp>5 and bag()==[(POTION,2)],(hp,bag())
    print('PASS items still work outside the chamber',flush=True)
    close_menus()
    for black in (0,1):
        load('pallet_with_ghost');m[0xd455]=100;m[0xd456]=0;m[0xd46c]=black;m[RIT]=6 if black else 0
        for k in range(8):
            p.button('left' if k%2==0 else 'right',8);T(24)
        print('BLACK=%d: hunger after 8 steps'%black,m[0xd455],'step counter',m[0xd456])
        assert (m[0xd455]==100)==(black==1),(black,m[0xd455])
    print('PASS the hunger engine runs normally and is off for BLACK',flush=True)
elif MODE=='you':
    import json
    from PIL import Image
    L=json.load(open('manifest_v25.json'))['labels']['bank2d'];ys=int(L['you_struct'],16)
    ystruct=bytes(ROM_BYTES[0x2d*0x4000+ys-0x4000:0x2d*0x4000+ys-0x4000+44])
    shots={}
    for tag,black in (('red',0),('black',1)):
        load('pallet_with_ghost');m[0xd455]=255;m[0xd46c]=black;m[RIT]=6 if black else 0
        m[0xd163]=1;m[0xd164]=YOU;m[0xd165]=0xff;m[0xd16b:0xd16b+44]=ystruct
        m[0xd273:0xd27e]=m[0xd158:0xd163];m[0xd2b5:0xd2c0]=m[0xd158:0xd163]
        m[0xd177]=m[0xd359];m[0xd178]=m[0xd35a]
        m[0xd059]=0x24;m[0xd127]=5
        for k in range(1500):
            p.tick();b=clean(box())
            if m[0xd057] and 'Go' in b:T(70);break
        assert wait_menu();im=p.screen.image.copy();im.save(S+'v25_you_%s.png'%tag)
        shots[tag]=dark_ratio(im,(0,50,80,100));print(tag,'YOU back pic dark ratio',round(shots[tag],2),'mon',hex(m[0xd014]))
        assert m[0xd014]==YOU
    assert shots['black']>shots['red']+0.05,shots
    print('PASS the stand-in YOU is drawn with the BLACK back picture when BLACK (RED back picture otherwise)',flush=True)
elif MODE=='shots':
    from PIL import Image
    def setup():m[RIT]=6;m[0xd465]=2
    warp(0x25,0,setup);bfs_to(6,6);p.button('up',8);T(30);press_('a',70);a=p.screen.image.copy()
    press_('a',70);press_('a',70);b=p.screen.image.copy()
    load('v25_black_'+ROMTAG);T(30);bfs_to(18,11);p.button('down',16)
    got=[]
    for k in range(3000):
        T(1)
        if m[0xd35e]==0x94 and k>60 and box() and len(got)<3 and k%260==200:got.append(p.screen.image.copy())
        if box() and k%50==20:p.button('a',8)
        if m[0xd46f]==3:break
    ims=[a,b]+got[:2]
    c=Image.new('RGB',(len(ims)*330,288),'white')
    for i,im in enumerate(ims):c.paste(im.convert('RGB').resize((320,288),Image.NEAREST),(i*330,0))
    c.save(S+'v25_scenes.png')

elif MODE=='backpic':
    # v26: BLACK's back picture has an empty margin (no halo/silhouette in the outer 2 px) so it can't look like a square
    import json
    sys.path.insert(0,'../ref');import pic,red_ghost_fusion as FZ
    info=json.load(open('manifest_v26.json'))['back_pic'];addr=int(info['addr'],16)
    g=FZ.grid(ROM_BYTES,0x2d,addr);H=W=len(g);assert H==32
    edge=[(y,x) for y in range(H) for x in range(W) if min(y,x,H-1-y,W-1-x)<2]
    bad=[(y,x) for y,x in edge if g[y][x]]
    dark=sum(1 for row in g for c in row if c==3)
    print('back pic %dx%d, dark pixels %d, non-white pixels in the outer 2 px: %d'%(H,W,dark,len(bad)))
    assert not bad and 250<dark<600
    print('PASS BLACK back picture: margin is empty (no square), silhouette still solid',flush=True)
