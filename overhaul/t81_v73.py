# v73: PRETA's sight text, AGATHA / FUJI lines, the SAFFRON shamaness's new place, a cursed SNORLAX
#  snorlax - ROUTE 12 / 16 after-battle scripts: the "returned to the mountains" text is shown, unless CURSE was used (flags happen either way)
#  scope   - the Marowak ghost branch of PrintBeginningBattleText: PRETA in the party -> "PRETA's sight unveiled...", the real SILPH SCOPE -> the old text
#  fuji    - FUJI at home, after the FLUTE: the AGATHA line on the GHOST route only
#  hostage - AGATHA's 7F text without "tied"
#  saffron - the shamaness is not at SILPH CO.'s door any more
import sys
MODE81=sys.argv[1]
sys.argv=['t79_v71.py','none']
exec(open('t79_v71.py').read().split("if MY=='gates':")[0])
MY=MODE81
def run_script(var,val,frames=700):
    m[var]=val;m[0xda39]=val;seen.clear()
    for i in range(frames//10):
        T(10)
        if m[var]==0:break
    for i in range(40):
        if m[var]==0 and not box():break
        press_('a',60)
    return allt().replace("'","")
if MY=='snorlax':
    for mp,var,flagaddr,flagbit,key in ((0x17,0xd624,0xd7d8,0x80,'returned'),(0x1b,0xd626,0xd7e0,0x02,'returned')):
        for cursed in (False,True):
            warp_from_pallet(mp,0);m[0xd887]=0
            m[flagaddr]&=~flagbit;m[0xd057]=0;m[0xcf0b]=0;m[0xd452]=1 if cursed else 0
            t=run_script(var,3)
            k='%02x %s'%(mp,'cursed' if cursed else 'not cursed')
            print(k,'text:',t[-120:],flush=True)
            ok(bool(m[flagaddr]&flagbit),'%s: the event flag is set (SNORLAX is gone)'%k)
            ok(m[var]==0,'%s: the map script is finished'%k)
            if cursed:ok(sum(c.isalpha() for c in t)<3,'%s: no "returned to the mountains" text'%k)
            else:ok('yawn' in t,'%s: the usual text'%k)
elif MY=='scope':
    import random
    hook_on=[False]
    def force(ctx):
        if hook_on[0]:m[0xcfd8]=0x91
    p.hook_register(0x16,0x4ddd,force,None)
    def battle(with_preta,with_scope):
        random.seed(4)
        warp_from_pallet(0x90,0);m[0xd887]=0
        if with_preta:m[0xd163]=2;m[0xd164]=0x1f;m[0xd165]=0xb6;m[0xd166]=0xff
        else:m[0xd163]=1;m[0xd164]=0x1f;m[0xd165]=0xff
        m[0xd31d]=1 if with_scope else 0
        if with_scope:m[0xd31e]=0x48;m[0xd31f]=1;m[0xd320]=0xff
        hook_on[0]=True
        for i in range(2500):
            if m[0xd057]:break
            m[0xd0db]=0;m[0xd455]=255;walk(random.choice(['up','down','left','right']),1)
        seen.clear()
        for i in range(40):
            b=box()
            if b and (not seen or seen[-1]!=b):seen.append(b)
            if 'FIGHT' in b:break
            p.button('a',8);p.tick(90)
        hook_on[0]=False
        return allt().replace("'","")
    t=battle(True,False);print('PRETA:',t[-200:],flush=True)
    ok("PRETA" in t and 'unveiled' in t and 'SILPH SCOPE' not in t,'PRETA in the party: its own unveiling text')
    t=battle(False,True);print('SCOPE:',t[-200:],flush=True)
    ok('SILPH SCOPE' in t and 'unveiled' in t and 'PRETA' not in t,'the real SILPH SCOPE: the original text')
elif MY=='fuji':
    def talk5(ghost,black=0,agatha_gone=0):
        load('pallet_with_ghost');lead(0x1f);m[0xd16b+29]=0x3f;m[0xd455]=255;m[0xd769]|=0x80;m[0xd5ae]&=0xef
        for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=0;m[0xd3af+4*i+3]=0x95
        for i in range(6):
            if m[0xd35e]==0x95:break
            walk('up',1)
        T(120);m[0xd887]=0
        m[0xd76c]|=1;m[0xd451]=1 if ghost else 0;m[0xd46c]=black;m[0xd466]=0x02 if agatha_gone else 0
        bfs_to(2,3,maxn=600);p.button('up',8);T(20);seen.clear()
        for k in range(30):
            if (not box() and k>12):break
            press_('a',70)
        return allt().replace("'","")
    t=talk5(True);print('GHOST route:',t[-260:],flush=True)
    ok('AGATHA' in t and 'thanks' in t and 'FLUTE helped' in t,'GHOST route: FUJI mentions AGATHA and the thanks')
    t=talk5(False);ok('FLUTE helped' in t and 'AGATHA' not in t,'no GHOST: the usual line')
    t=talk5(True,black=1);ok('FLUTE helped' in t and 'AGATHA' not in t,'BLACK: the usual line')
    t=talk5(True,agatha_gone=1);ok('FLUTE helped' in t and 'AGATHA' not in t,'AGATHA gone: the usual line')
elif MY=='hostage':
    d=open(os.environ['CB_ROM'],'rb').read() if False else None
    import os
    rom=open(os.environ['CB_ROM'],'rb').read()
    s=0x2e*0x4000+0x6a7c-0x4000
    t=bytes(rom[s:s+90])
    from patchlib import enc
    ok(t.find(enc('tied'))<0 and t.find(enc('Hmph!'))>0,'AGATHA\'s 7F hostage text has no "tied"')
elif MY=='saffron':
    warp_from_pallet(0x0a,0);m[0xd887]=0;m[0xd451]=1
    sp=[(i,hex(m[0xc100+16*i]),m[0xc204+16*i]-4,m[0xc205+16*i]-4) for i in range(1,m[0xd4e1]+1)]
    sh=[s for s in sp if s[1]=='0x19' and m[0xd4e4+2*(s[0]-1)+1]==0x3f]
    print('shamaness',sh,flush=True)
    ok(len(sh)==1 and (sh[0][2],sh[0][3])==(24,32),'the SAFFRON shamaness stands at (24,32)')
    ok(not any((s[2],s[3])==(22,19) and s[1]!='0x0' for s in sp),'nobody stands at SILPH CO.\'s door tile (22,19)')
print('t81 done',flush=True)
