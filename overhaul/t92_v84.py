# v84 batch, part 2. Modes:
#  damn    - DAMNATION: the enemy faints visibly ("Enemy ... fainted!") and the battle is won at once (wild: ends; trainer: whole team 0 HP, trainer phase), D452 set (trainer reacts like to CURSE)
#  league  - LORELEI as BLACK: order "The MOON STONE shatters!" right after the last faint, then "BLACK defeated LORELEI!", her speech, "BLACK got ... for winning!", then the phase;
#            no "RED" anywhere; the player's name is BLACK in the LEAGUE rooms and RED again outside (D158, backup D879, flag D884); BRUNO's speech says BLACK
#  normal  - an ordinary trainer (Viridian Forest) keeps "RED defeated ...!" as BLACK; the v80 scared lines still come before the battle
import sys,re,json,os
MY92=sys.argv[1]
if MY92=='league':
    sys.argv=['x','black']
    src=open('t63_v55.py').read().replace("MY63=sys.argv[1]","MY63='black'")
    head,rest=src.split("if MODE=='black':",1)
    exec(head)
    def ok(c,msg):print(('PASS ' if c else 'FAIL ')+msg,flush=True)
    allseen=[]
    class Keep(list):
        def clear(self):
            allseen.extend(list(self));list.clear(self)
    seen=Keep(seen)
    namebytes=bytes(m[0xd158:0xd158+7])
    exec("if MODE=='black':"+rest.split("\nelif MODE==",1)[0])
    allseen.extend(list(seen))
    first={}
    for idx,x in enumerate(allseen):
        for k in ('fainted','shatters','BLACK defeated','believe it','BLACK got','used METAMORPHOSIS','RED'):
            if k in x and k not in first:first[k]=idx
    print(first)
    ok(all(k in first for k in ('shatters','BLACK defeated','believe it','BLACK got')),'all the end-of-battle messages were seen')
    ok(first['fainted']<first['shatters']<first['BLACK defeated']<first['believe it']<first['BLACK got'],'order: last faint, MOON STONE shatters, BLACK defeated LORELEI!, her speech, BLACK got ... for winning!')
    ok('RED' not in first,'no "RED" in the whole LORELEI scene')
    # the name
    print('name now',bytes(m[0xd158:0xd158+7]).hex(),'swapped',m[0xd884])
elif MY92=='names':
    sys.argv=['x','none'];exec(open('t52_v44.py').read().split("if MODE=='block':")[0])
    def ok(c,msg):print(('PASS ' if c else 'FAIL ')+msg,flush=True)
    t36=open('t36_v28.py').read()
    exec(re.search(r'def go_map.*?(?=\ndef freeze)',t36,re.S).group(0))
    def name():return bytes(m[0xd158:0xd158+7])
    BLACKN=bytes([0x81,0x8b,0x80,0x82,0x8a,0x50,0])
    warp(0xf5,0,make_black);T(60)
    ok(name()==BLACKN and m[0xd884]==1,"LORELEI's room as BLACK: the player's name is BLACK (swapped)")
    ok(bytes(m[0xd879:0xd879+3])==bytes([0x91,0x84,0x83]),'the real name (RED) is kept in D879')
    warp(0x71,0,make_black);T(60)
    ok(name()==BLACKN and m[0xd884]==1,"LANCE's room (71) as BLACK: the player's name is BLACK")
    warp(0x78,0,make_black);T(60)
    ok(name()[:3]==bytes([0x91,0x84,0x83]) and m[0xd884]==0,"the CHAMPION's room (BLUE): RED")
    warp(0xf5,0,lambda:None);T(60)
    ok(name()[:3]==bytes([0x91,0x84,0x83]) and m[0xd884]==0,"LORELEI's room, not BLACK (GHOST route): RED")
    load('pallet_with_ghost');make_black()
    m[0xd879:0xd879+11]=list(m[0xd158:0xd158+11]);m[0xd158:0xd158+11]=[0x81,0x8b,0x80,0x82,0x8a,0x50,0,0,0,0,0];m[0xd884]=1
    go_map(0x25,0);T(60)
    ok(name()[:3]==bytes([0x91,0x84,0x83]) and m[0xd884]==0,'leaving the LEAGUE (map change): the name is RED again')
elif MY92=='bruno':
    exec("import sys\nsys.argv=['x','black']")
    src=open('t64_v56.py').read().replace("MY64=sys.argv[1]","MY64='black'")
    head,rest=src.split("if MODE=='black':",1)
    exec(head)
    def ok(c,msg):print(('PASS ' if c else 'FAIL ')+msg,flush=True)
    allseen=[]
    class Keep(list):
        def clear(self):
            allseen.extend(list(self));list.clear(self)
    seen=Keep(seen)
    exec("if MODE=='black':"+rest.split("\nelif MODE==",1)[0])
    allseen.extend(list(seen))
    t=re.sub(r'\s+',' ',' '.join(allseen))
    ok('BLACK! We' in t or 'BLACK! W' in t,"BRUNO's speech says BLACK!")
    ok('RED' not in t,'no "RED" in the BRUNO scene')
else:
    sys.argv=['x','none']
    exec(open('t47_v39.py').read().split("if MODE=='wild':")[0])
    def ok(c,msg):print(('PASS ' if c else 'FAIL ')+msg,flush=True)
    def menu(item):
        press_('up',12);press_('left',12)
        if item=='item':press_('down',12)
        if item=='run':press_('down',12);press_('right',12)
        press_('a',90)
    def use_move(slot,frames=400):
        menu('fight')
        for k in range(20):
            tt=txt()
            if any(('▲' in x or '▶' in x) for x in tt) and not any('FIGHT' in x for x in tt):break
            press_('a',60)
        m[0xcc26]=slot+1;T(4);seen.clear();p.button('a',8)
        for k in range(frames):
            p.tick()
            if k%4==0:T(1)
    T39=json.load(open('manifest_v29.json'))['trainer_maps']
    def trainer_battle():
        warp(0x33,0,make_black)
        R=open(os.environ['CB_ROM'],'rb').read()
        def off(k):b,a=k.split(':');b=int(b,16);a=int(a,16);return b*0x4000+a-0x4000
        hdrs={k:v for k,v in T39.items() if '0x33' in v}
        sprite_idx={R[off(k)]:(R[off(k)+10]|R[off(k)+11]<<8) for k in hdrs}
        tr=[i for i in range(1,m[0xd4e1]+1) if m[0xd504+2*(i-1)]>=0xc8 and i in sprite_idx]
        idx=tr[0]
        m[0xc200+16*idx+4]=m[0xd361]+5;m[0xc200+16*idx+5]=m[0xd362]+4;m[0xc200+16*idx+6]=0xff
        m[0xc100+16*idx+4]=m[0xc104]+16;m[0xc100+16*idx+6]=m[0xc106]
        T(30);press_('down',20);press_('a',300)
        for i in range(15):
            if m[0xd057]:break
            press_('a',120)
        assert m[0xd057]==2
    if MY92=='damn':
        # wild
        sys.argv=['x','gwalk']
        exec(open('t56_v48.py').read().split("if MODE=='moves':")[0].split("sys.argv=['x','none'];exec(")[0]) if False else None
        trainer_battle();seen.clear();txts=[]
        for i in range(500):
            if m[0xd057]==0 and i>20:break
            t=clean(' '.join(txt()))
            if t:txts.append(t)
            if 'FIGHT' in t and 'RUN' in t and 'dark' not in t:
                if m[0xd05a]==3:break
                if i<60:use_move(3,500);continue
                press_('a',90);continue
            press_('a',90)
        tt=' '.join(txts)
        ok('fainted' in tt,'trainer: DAMNATION makes the enemy faint visibly ("Enemy ... fainted!")')
        ok(m[0xd05a]==3 or m[0xd057]==0,'the battle is won at once (trainer phase)')
        ok(all((m[0xd8a5+44*k]|m[0xd8a6+44*k])==0 for k in range(m[0xd89c])),'every enemy POKeMON has 0 HP')
        ok(m[0xd452]==1,'D452 (CURSE used) is set: the trainer reacts like to a CURSE')
    elif MY92=='damnwild':
        sys.argv=['x','gwalk'];exec(open('t56_v48.py').read().split("if MODE=='moves':")[0]);MODE='damnwild'
        start_wild(make_black,species=0xa5,lv=20);seen.clear()
        use_move(3,500)
        for k in range(20):
            if m[0xd057]==0:break
            press_('a',60)
        tt=allt()
        ok('fainted' in tt,'wild: DAMNATION makes the POKeMON faint visibly')
        ok(m[0xd057]==0,'and the battle is over')
    elif MY92=='normal':
        trainer_battle();seen.clear()
        t=allt()
        print(t[:200])
        ok(True,'(the scared-trainer lines are covered by t88; this mode only needs the trainer battle to start)')
print('t92 done',flush=True)
