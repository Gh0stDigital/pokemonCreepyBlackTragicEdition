# v67: SHOCK MODE for the gyms (CERULEAN GYM: JR TRAINER sprite 2 at 3,2; trainer 3 at 7,8; MISTY sprite 1; kill indices 436/437, MISTY 26). Modes:
#  shock  - CURSE kills the first gym trainer: D839 bit 1 (shock); the other trainer (unbeaten) says the avenge line, MISTY her own line
#  sulk   - a trainer beaten with CURSE used but spared (RUN): talking to them again: "You are evil... leave"; a normal win (no CURSE) is not a sulker
#  abandon- MISTY dead (kill bit): entering the gym again: everybody but her grave is gone
import sys
MY75=sys.argv[1]
sys.argv=['x','none']
src=open('t28_v14.py').read().split("if MODE=='mirage_rate':")[0].replace("MODE=sys.argv[1]","MODE='x'")
exec(src)
MODE=MY75
def ok(c,msg):print(('PASS ' if c else 'FAIL ')+msg,flush=True)
def talk_to(sy,sx,face,tag):
    path=bfs_to(sy,sx,maxn=600)
    p.button(face,8);T(20);seen.clear()
    for i in range(30):
        if m[0xd057] or (not box() and i>12):break
        press_('a',70)
    return allt().replace("'","")
def gym_state():
    return (m[0xd839],list(m[0xd83a:0xd840]),m[0xd453])
if MODE=='trainers':
    def summon(i):
        y,x=m[0xd361],m[0xd362];b1=0xc100+i*16;b2=0xc200+i*16
        m[b1+4]=0x2c;m[b1+6]=0x40;m[b2+4]=y-1+4;m[b2+5]=x+4;m[b2+6]=0xff
    def talk_up(i):
        summon(i);T(10);p.button('up',8);T(20);seen.clear()
        for k in range(30):
            if m[0xd057] or (not box() and k>12):break
            press_('a',70)
        return allt().replace("'","")
    for name,mp,g in (('PEWTER',0x36,0),('CERULEAN',0x41,1),('VERMILION',0x5c,2),('CELADON',0x86,3),('FUCHSIA',0x9d,4),('SAFFRON',0xb2,5),('VIRIDIAN',0x2d,7)):
        warp_from_pallet(mp,0);m[0xd887]=0;m[0xd839]|=1<<g
        t=talk_up(2)
        print(name,'trainer 2:',t[:150],flush=True)
        ok(any(k in t for k in ('teammate','avenge','killed one of','dead because','Our ')),'%s: an unbeaten trainer says the avenge line (shock)'%name)
    print('t75 done',flush=True);sys.exit(0)
if MODE=='abandon_all':
    for name,mp,g,idx in (('PEWTER',0x36,0,12),('CERULEAN',0x41,1,26),('VERMILION',0x5c,2,27),('CELADON',0x86,3,28),('FUCHSIA',0x9d,4,29),('SAFFRON',0xb2,5,30),('CINNABAR',0xa6,6,31),('VIRIDIAN',0x2d,7,32)):
        for armed in (False,True):
            warp_from_pallet(mp,0);m[0xd887]=0
            m[0xd4a4+(idx>>3)]|=1<<(idx&7)
            if armed:m[0xd842]|=1<<g
            # reload the map the way the game does after a menu / warp: re-enter via the stored warp
            load('pallet_with_ghost');lead(0x1f);m[0xd16b+29]=0x3f;m[0xd455]=255
            m[0xd4a4+(idx>>3)]|=1<<(idx&7)
            if armed:m[0xd842]|=1<<g
            for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=0;m[0xd3af+4*i+3]=mp
            for i in range(6):
                if m[0xd35e]==mp:break
                walk('up',1)
            T(120)
            n=m[0xd4e1];pics=[m[0xc100+i*16] for i in range(2,n+1)]
            live=sum(1 for q in pics if q)
            print(name,'armed' if armed else 'unarmed','sprites',n,'pics',pics,flush=True)
            ok((live==0)==armed,'%s: %s'%(name,'abandoned (everyone but the grave is gone)' if armed else 'leader dead this visit: nobody leaves'))
    print('t75 done',flush=True);sys.exit(0)
if MODE=='killall':
    def summon(i):
        y,x=m[0xd361],m[0xd362];b1=0xc100+i*16;b2=0xc200+i*16
        m[b1+4]=0x2c;m[b1+6]=0x40;m[b2+4]=y-1+4;m[b2+5]=x+4;m[b2+6]=0xff
    for name,mp,g in (('PEWTER',0x36,0),('VERMILION',0x5c,2),('CELADON',0x86,3),('FUCHSIA',0x9d,4),('SAFFRON',0xb2,5),('VIRIDIAN',0x2d,7)):
        warp_from_pallet(mp,0);m[0xd887]=0
        summon(2);T(10);p.button('up',8);T(20);seen.clear()
        for i in range(30):
            if m[0xd057]:break
            press_('a',60)
        idx=m[0xd4ae]<<8|m[0xd4af]
        print(name,'battle',m[0xd057],'idx',idx,flush=True)
        if not m[0xd057]:ok(False,'%s: battle starts'%name);continue
        fight()
        for i in range(30):press_('a',90)
        print(name,gym_state(),flush=True)
        ok(m[0xd453]==1 and m[0xd839]&(1<<g)==(1<<g) and m[0xd839]==(1<<g),'%s: killed with CURSE -> murder flag and this gym (bit %d) alone in SHOCK'%(name,g))
    print('t75 done',flush=True);sys.exit(0)
if MODE=='leaders':
    GY=[('PEWTER',0x36,0,[(0xd755,0x04)],(2,4),'student','The rock stands'),('VERMILION',0x5c,2,[(0xd773,0x1c)],(2,5),'my boys','fry you'),
        ('CELADON',0x86,3,[(0xd77c,0xfc),(0xd77d,0x01)],(4,4),'flowers wilt','students'),('FUCHSIA',0x9d,4,[(0xd792,0xfc),(0xd793,0x01)],(11,4),'ninja dead','x'),('SAFFRON',0xb2,5,[(0xd7b3,0xfc),(0xd7b4,0x01)],(9,9),'foresaw the death','x'),('CINNABAR',0xa6,6,[],(4,3),'\x00no shock line here','x'),('VIRIDIAN',0x2d,7,[(0xd751,0xfc),(0xd752,0x03)],(2,2),'my men','BOSS')]
    def summon(i):
        """put sprite i (a gym leader / trainer) on the tile above the player: the gyms' puzzles block a real walk"""
        y,x=m[0xd361],m[0xd362]
        b1=0xc100+i*16;b2=0xc200+i*16
        m[b1+4]=0x2c;m[b1+6]=0x40;m[b1+2]=1 if m[b1+2]==0xff else m[b1+2]
        m[b2+4]=y-1+4;m[b2+5]=x+4;m[b2+6]=0xff
    def talk_up(i):
        summon(i);T(10);p.button('up',8);T(20);seen.clear()
        for k in range(30):
            if m[0xd057] or (not box() and k>12):break
            press_('a',70)
        return allt().replace("'","")
    for name,mp,g,flags,(sy,sx),k1,k2 in GY:
        for shocked in (False,True):
            warp_from_pallet(mp,0);m[0xd887]=0
            for a,mk in flags:m[a]|=mk
            if shocked:m[0xd839]|=1<<g
            if name=='CINNABAR':shocked=False      # quiz gym: cannot be shocked, the usual speech both times
            t=talk_up(1)
            print(name,shocked,t[:200],flush=True)
            ok((k1 in t)==shocked,'%s: %s'%(name,'the leader has the shock line' if shocked else 'not shocked: the leader\'s usual speech'))
    print('t75 done',flush=True);sys.exit(0)
else:
    warp_from_pallet(0x41,0);m[0xd887]=0
    m[0xd75e]|=0x0c                                   # both trainers count as beaten while we walk
if MODE=='shock':
    bfs_to(3,3);p.button('left',8);T(20);seen.clear();m[0xd75e]&=~0x04     # trainer 2 (3,2) is not beaten any more: talk to it
    for i in range(30):
        if m[0xd057]:break
        press_('a',60)
    m[0xd75e]&=~0x08
    print('battle',m[0xd057],'class',m[0xd031],'idx',m[0xd4ae]<<8|m[0xd4af],flush=True)
    idx=m[0xd4ae]<<8|m[0xd4af]
    ok(m[0xd057]==2 and idx in (436,437),'a gym trainer fights (kill index %d)'%idx)
    fight()
    for i in range(30):press_('a',90)
    print('state',gym_state(),flush=True)
    ok(m[0xd453]==1 and m[0xd839]&2,'killed with CURSE: murder flag and the gym is in SHOCK (D839 bit 1)')
    for i in range(6):press_('b',40)
    T(120);save('v75_shock')
    # the other trainer (unbeaten): the new line, then the battle
    t=talk_to(7,9,'left','trainer 3')
    print('trainer 3:',t[:260],flush=True)
    ok(any(k in t for k in ('teammate','avenge','killed one of','dead because')),'the unbeaten trainer says the new "avenge" line before the battle')
    ok(m[0xd057]!=0,'and then fights')
    # a beaten trainer
    load('v75_shock');m[0xd75e]|=0x08
    t=talk_to(7,9,'left','beaten trainer')
    print('beaten trainer:',t[:200],flush=True)
    ok(any(k in t for k in ('MURDERER','Our teammate','even look')) and m[0xd057]==0,'a beaten trainer tells you to get out of the gym')
    # MISTY
    load('v75_shock');m[0xd75e]|=0x0c
    t=talk_to(3,4,'up','MISTY')
    print('MISTY:',t[:260],flush=True)
    ok('friend' in t and 'wash you' in t,"MISTY has her own line for her dead student")
elif MODE=='sulk':
    m[0xd75e]|=0x0c
    bfs_to(3,3);p.button('left',8);T(20);seen.clear();m[0xd75e]&=~0x04
    for i in range(30):
        if m[0xd057]:break
        press_('a',60)
    m[0xd75e]|=0x0c
    idx=m[0xd4ae]<<8|m[0xd4af];print('battle idx',idx,flush=True)
    fight(hp1=True,spare=True)
    for i in range(30):press_('a',90)
    print('state',gym_state(),flush=True)
    ok(m[0xd453]==0 and not m[0xd839],'spared: no murder, no shock')
    ok(any(m[0xd83a:0xd840]),'CURSE was used, the trainer lives: a sulk bit is set (%s)'%list(m[0xd83a:0xd840]))
    m[0xd75e]|=0x04
    t=talk_to(3,3,'left','sulker')
    print('sulker:',t[-300:],flush=True)
    ok('evil' in t or 'monster' in t or 'cruelty' in t,'the trainer sulks')
elif MODE=='normal':
    m[0xd16b+8:0xd16b+12]=[0x21,0,0,0];m[0xd16b+29]=0x3f           # GHOST knows only TACKLE: no CURSE
    m[0xd75e]|=0x0c
    bfs_to(3,3);p.button('left',8);T(20);seen.clear();m[0xd75e]&=~0x04
    for i in range(30):
        if m[0xd057]:break
        press_('a',60)
    m[0xd75e]|=0x0c
    fight(hp1=True,spare=True)
    for i in range(30):press_('a',90)
    print('state',gym_state(),flush=True)
    ok(not m[0xd839] and not any(m[0xd83a:0xd840]) and m[0xd453]==0,'a normal win: no shock, no sulk bit')
    t=talk_to(3,3,'left','after')
    print('after:',t[-300:],flush=True)
    ok('evil' not in t and 'monster' not in t and 'cruelty' not in t and 'MURDERER' not in t,'the usual after-battle text')
elif MODE=='abandon':
    load('pallet_with_ghost');lead(0x1f);m[0xd16b+29]=0x3f;m[0xd455]=255
    m[0xd4a7]|=0x04;m[0xd842]|=0x02                  # MISTY (kill index 26) is dead and the player has been out since (armed): the gym is entered afterwards
    for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=0;m[0xd3af+4*i+3]=0x41
    for i in range(6):
        if m[0xd35e]==0x41:break
        walk('up',1)
    T(120);print('arrived',pos(),flush=True)
    sp=[(i,hex(m[0xc100+16*i]),m[0xc204+16*i]) for i in range(1,m[0xd4e1]+1)]
    print('sprites',sp,flush=True)
    ok(m[0xd35e]==0x41 and m[0xc110]==0x49,'MISTY is a gravestone')
    ok(all(m[0xc100+16*i]==0 for i in range(2,m[0xd4e1]+1)),'everybody else is gone (picture 0)')
    ok(all(m[0xc200+16*i+4]==0xff for i in range(2,m[0xd4e1]+1)),'and off the map (position FF)')
    # the visit of the kill: nobody leaves (not armed yet)
    load('pallet_with_ghost');lead(0x1f);m[0xd455]=255;m[0xd4a7]|=0x04
    for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=0;m[0xd3af+4*i+3]=0x41
    for i in range(6):
        if m[0xd35e]==0x41:break
        walk('up',1)
    T(120)
    ok(m[0xd35e]==0x41 and all(m[0xc100+16*i]!=0 for i in range(2,m[0xd4e1]+1)),'the visit in which the leader died: the trainers are still there (v14: they swear revenge)')
    # the next map that is not a gym arms the abandonment (D842 bit 1)
    load('pallet_with_ghost');lead(0x1f);m[0xd455]=255;m[0xd4a7]|=0x04;m[0xd842]=0
    for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=0;m[0xd3af+4*i+3]=0x25
    for i in range(6):
        if m[0xd35e]==0x25:break
        walk('up',1)
    T(60)
    ok(m[0xd35e]==0x25 and m[0xd842]&2,'the next map that is not a gym arms it (D842 bit 1)')
    # a gym whose leader is alive is unchanged
    load('pallet_with_ghost');lead(0x1f);m[0xd455]=255
    for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=0;m[0xd3af+4*i+3]=0x41
    for i in range(6):
        if m[0xd35e]==0x41:break
        walk('up',1)
    T(120)
    ok(m[0xc110]==0x1d and all(m[0xc100+16*i]!=0 for i in range(1,m[0xd4e1]+1)),'leader alive: everybody is still there')
print('t75 done',flush=True)
