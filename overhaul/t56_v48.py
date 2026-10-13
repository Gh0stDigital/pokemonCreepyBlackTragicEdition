# v48: BLACK's new moves and the negative animations. Modes:
#  moves    - after a step BLACK knows METAMORPHOSIS, CURSE, GHOST WALK, DAMNATION (full PP); the battle move menu lists them
#  gwalk    - GHOST WALK on a wild RATTATA: turn 1 "faded into dark!" + TELEPORT's animation in the negative palette,
#             turn 2 CUT's animation, negative, RATTATA loses HP; the palette is normal again after each animation
#  damnwild - DAMNATION on a wild RATTATA: HYPER BEAM's animation (normal palette), the battle ends like a CURSE
#  damntr   - DAMNATION in a trainer battle (Viridian Forest): the trainer's whole team dies at once, the battle is won
#             (trainer phase), every enemy POKeMON has 0 HP
#  macabre  - PRETA's MACABRE: CRABHAMMER's animation, negative; AZHI's BLACK FLAME: FIRE BLAST's, negative
#  normal   - CHARMANDER's SCRATCH: its own animation in the normal palette
#  azhi     - AZHI (ritual struct) knows BLACK FLAME (10 PP), FLY, DRAGON RAGE, SKY ATTACK; the MIRAGE's AZHI too
#  moon     - LORELEI as BLACK: DAMNATION is blocked by the MOON STONE like the other death moves
import sys,json
MY56=sys.argv[1]
sys.argv=['x','none'];exec(open('t52_v44.py').read().split("if MODE=='block':")[0]);MODE=MY56
META,CURSE,GWALK,DAMN=0xaa,0xa5,0xab,0xac
anims=[];after=[]
p.hook_register(0x1e,0x40f1,lambda c:anims.append((m[0xd07c],p.memory[0xff47])),None)
p.hook_register(0x1e,0x4d9b,lambda c:after.append(p.memory[0xff47]),None)
def start_wild(setup,species=0xa5,lv=5):
    load('pallet_with_ghost');setup();m[0xd059]=species;m[0xd127]=lv
    for i in range(300):
        if m[0xd057]:break
        p.tick()
    wait_menu();T(20)
def run_move(slot,turns=1):
    for t in range(turns):
        wait_menu()
        if m[0xd057]==0:return
        use_move(slot,400)
        for k in range(10):
            tt=clean(' '.join(txt()))
            if ('FIGHT' in tt and 'RUN' in tt) or m[0xd057]==0:break
            press_('a',70)
def lead_struct(struct):
    make_black();m[0xd16b:0xd16b+44]=list(struct);m[0xd164]=struct[0];m[0xd16b+12]=m[0xd359];m[0xd16b+13]=m[0xd35a]   # the player's OT: obeys
if MODE=='moves':
    load('pallet_with_ghost');make_black();p.button('up',8);T(30);p.button('down',8);T(30)
    mv=list(m[0xd16b+8:0xd16b+12]);pp=list(m[0xd16b+29:0xd16b+33]);print('moves',[hex(x) for x in mv],pp)
    ok(mv==[META,CURSE,GWALK,DAMN] and pp==[10,1,15,1],'BLACK knows METAMORPHOSIS, CURSE, GHOST WALK, DAMNATION (full PP)')
    start_wild(make_black);menu('fight');T(30);t=' '.join(txt());print(t)
    ok(all(n in t for n in ('METAMORPHOSIS','CURSE','GHOST WALK','DAMNATION')),'the move menu lists all four')
elif MODE=='gwalk':
    start_wild(make_black,lv=40);h0=ehp();anims.clear();after.clear();seen.clear()
    use_move(2,400)
    for k in range(12):
        if 'dark!' in allt():break
        press_('a',40)
    t1=list(anims);print('turn 1',[(hex(a),hex(b)) for a,b in t1],allt()[-120:])
    ok('faded into dark' in allt(),'turn 1: "BLACK faded into dark!"')
    ok((0x64,0x1b) in t1,"turn 1: TELEPORT's animation in the negative palette (BGP 1B)")
    anims.clear()
    for k in range(40):
        if any(a==0x0f for a,b in anims) or m[0xd057]==0:break
        tt=clean(' '.join(txt()))
        if 'FIGHT' in tt and 'RUN' in tt:press_('a',90);continue
        press_('a',60)
    for k in range(6):press_('a',60)
    print('turn 2',[(hex(a),hex(b)) for a,b in anims],'enemy HP',h0,'->',ehp(),'after',[hex(x) for x in after])
    ok((0x0f,0x1b) in anims,"turn 2: CUT's animation in the negative palette")
    ok(ehp()<h0,'RATTATA lost HP (%d -> %d)'%(h0,ehp()))
    ok(after and all(x==0xe4 for x in after),'the palette is normal after every animation')
elif MODE=='damnwild':
    start_wild(make_black);anims.clear();seen.clear();p0=party()
    use_move(3,500)
    for k in range(20):
        if m[0xd057]==0:break
        press_('a',60)
    print('anims',[(hex(a),hex(b)) for a,b in anims],allt()[-150:])
    ok('DAMNATION' in allt() and any(a==0x3f and b==0xe4 for a,b in anims),"DAMNATION: HYPER BEAM's animation (normal palette)")
    ok(m[0xd057]==0 and party()==p0,'the wild battle ends at once (the curse), nobody joins')
elif MODE=='damntr':
    T29=json.load(open('manifest_v29.json'))['trainer_maps']
    warp(0x33,0,make_black)
    R=open(os.environ['CB_ROM'],'rb').read()
    def off(k):b,a=k.split(':');b=int(b,16);a=int(a,16);return b*0x4000+a-0x4000
    hdrs={k:v for k,v in T29.items() if '0x33' in v}
    sprite_idx={R[off(k)]:(R[off(k)+10]|R[off(k)+11]<<8) for k in hdrs}
    tr=[i for i in range(1,m[0xd4e1]+1) if m[0xd504+2*(i-1)]>=0xc8 and i in sprite_idx]
    idx=tr[0]
    m[0xc200+16*idx+4]=m[0xd361]+5;m[0xc200+16*idx+5]=m[0xd362]+4;m[0xc200+16*idx+6]=0xff
    m[0xc100+16*idx+4]=m[0xc104]+16;m[0xc100+16*idx+6]=m[0xc106]
    T(30);press_('down',20);press_('a',300)
    for i in range(15):
        if m[0xd057]:break
        press_('a',120)
    ok(m[0xd057]==2,'trainer battle started')
    wait_menu();n=m[0xd89c];print('enemy party',[hex(m[0xd89d+i]) for i in range(n)])
    if n<2:                                          # make sure the trainer has a second POKeMON
        m[0xd89c]=2;m[0xd89d+1]=m[0xd89d];m[0xd89d+2]=0xff;m[0xd8a4+44:0xd8a4+88]=list(m[0xd8a4:0xd8a4+44]);n=2
    seen.clear();phase=[False];use_move(3,500)
    for i in range(300):
        if m[0xd05a]==3:phase[0]=True;break
        if m[0xd057]==0:break
        tt=clean(' '.join(txt()))
        if 'FIGHT' in tt and 'RUN' in tt:break
        press_('a',60)
    hps=[m[0xd8a5+44*i]<<8|m[0xd8a6+44*i] for i in range(n)];t=allt();print('HPs',hps,'phase',phase[0],t[-200:])
    ok('DAMNATION' in t,'"BLACK used DAMNATION!"')
    ok(all(h==0 for h in hps[1:]),'the rest of the trainer\'s team (%d) is dead at once'%(n-1))
    ok(phase[0],'the battle is won at once: the trainer phase starts')
elif MODE=='macabre':
    SA=fo(0x2d,int(L['s_azhi'],16))
    for struct,mv,an,name in ((ROM[SP:SP+44],0xa9,0x98,'PRETA MACABRE'),(ROM[SA:SA+44],0xa8,0x7e,'AZHI BLACK FLAME')):
        start_wild(lambda:lead_struct(struct),lv=40);anims.clear();after.clear();seen.clear()
        ok(m[0xd014]==struct[0] and m[0xd01c]==mv,'%s: out with the move in slot 1'%name)
        use_move(0,500)
        for k in range(6):press_('a',60)
        print(name,[(hex(a),hex(b)) for a,b in anims],[hex(x) for x in after])
        ok((an,0x1b) in anims,'%s: animation %s in the negative palette'%(name,hex(an)))
        ok(after and all(x==0xe4 for x in after),'%s: normal palette afterwards'%name)
elif MODE=='normal':
    start_wild(lambda:lead(CHAR));anims.clear();seen.clear()
    use_move(0,400)
    for k in range(6):press_('a',60)
    print([(hex(a),hex(b)) for a,b in anims])
    ok(any(a==0x0a and b==0xe4 for a,b in anims),"CHARMANDER's SCRATCH: its own animation, normal palette")
elif MODE=='azhi':
    SA=fo(0x2d,int(L['s_azhi'],16));s=ROM[SA:SA+44]
    ok(list(s[8:12])==[0xa8,0x13,0x52,0x8f] and s[29]==10 and s[32]&0x3f==5,'ritual AZHI: BLACK FLAME (10 PP), FLY, DRAGON RAGE, SKY ATTACK')
    ok(list(ROM[fo(0xe,0x7cc7):fo(0xe,0x7cc7)+4])==[0xa8,0x13,0x52,0x8f],"the MIRAGE's AZHI knows SKY ATTACK too")
elif MODE=='moon':
    to_battle(0xf5,3,5,make_black)
    ok(m[0xd031]==0x2c and m[0xd014]==BLK,'LORELEI battle, BLACK out')
    e0=ehp();m[0xd01c+3]=DAMN;m[0xd02d+3]=1;lo=use_move(3,300);read_until_menu();t=allt();print(t[-200:])
    ok('strange power' in t and 'DAMNATION' in t and ehp()==e0 and m[0xd057]==2,'DAMNATION is blocked by the MOON STONE (no turn, LORELEI unharmed)')
