# v69: an ordinary trainer you used CURSE on but spared sulks afterwards (one of 16 lines); without CURSE the usual text; killed ones still die; gym trainers untouched
import sys
MY=sys.argv[1]
sys.argv=['x','none']
src=open('t28_v14.py').read().split("if MODE=='mirage_rate':")[0].replace("MODE=sys.argv[1]","MODE='x'")
exec(src)
def ok(c,msg):print(('PASS ' if c else 'FAIL ')+msg,flush=True)
def summon(i):
    y,x=m[0xd361],m[0xd362];b1=0xc100+i*16;b2=0xc200+i*16
    m[b1+4]=0x2c;m[b1+6]=0x40;m[b2+4]=y-1+4;m[b2+5]=x+4;m[b2+6]=0xff
def talk_up(i):
    summon(i);T(10);p.button('up',8);T(20);seen.clear()
    for k in range(30):
        if m[0xd057] or (not box() and k>12):break
        press_('a',70)
    return allt().replace("'","")
SULK=('tell','Stay away','shaking','evil','rather','Don\'t talk','Nobody','What are you','eyes','scared','far from','done with','hands','frighten','monster','promise')
def is_sulk(t):return any(k in t for k in ('anyone, I swear','that thing did','shaking','Just go','again than','Don talk','Nobody will','What are you','its eyes','too scared','far from','done with battles','stop shaking','keep quiet','forget','Not a word'))
def first_trainer(mapid,spr,prep=None):
    warp_from_pallet(mapid,0);m[0xd887]=0
    m[0xd16b+1]=1;m[0xd16b+2]=0x2c;m[0xd16b+34]=1;m[0xd16b+35]=0x2c    # GHOST: 300 HP, it must survive
    if prep:prep()
    t=talk_up(spr)
    return (spr if m[0xd057] else None),t
def sbits():
    return sum(bin(m[a]).count('1') for a in list(range(0xd784,0xd78e))+list(range(0xd7a4,0xd7af))+list(range(0xd80a,0xd813))+list(range(0xd84f,0xd857))+list(range(0xd858,0xd85c)))
for MAP,SPR in ((0x0e,2),(0x0f,2)):
    print('=== map',hex(MAP),'sprite',SPR,flush=True)
    if MY=='sulk':
        i,t=first_trainer(MAP,SPR);print('trainer sprite',i,flush=True)
        ok(i is not None,'a trainer of the map starts a battle (sprite %s)'%i)
        idx=m[0xd4ae]<<8|m[0xd4af];print('kill index',idx,flush=True)
        fight(limit=1500,hp1=True,spare=True)
        for k in range(10):press_('b',60)
        ok(m[0xd453]==0,'spared: no murder')
        ok(m[0xd057]==0,'and the trainer does not challenge again (the beaten flag is set; v67/v68 lost it)')
        t=talk_up(i);print('after:',t[-250:],flush=True)
        ok(is_sulk(t),'the spared trainer sulks')
        # a different trainer who was not cursed keeps the usual text? (not fought) -> the dispatcher prints the original; check the sulk bit count
        import collections
        bits=sbits()
        ok(bits==1,'exactly one sulk bit is set (%d)'%bits)
    elif MY=='normal':
        def prep():m[0xd16b+8:0xd16b+12]=[0x21,0,0,0];m[0xd16b+29]=0x3f
        i,t=first_trainer(MAP,SPR,prep)
        ok(i is not None,'battle starts')
        fight(limit=1500,hp1=True,spare=True)
        for k in range(10):press_('b',60)
        ok(m[0xd057]==0,'a normal win: the trainer does not challenge again')
        t=talk_up(i);print('after:',t[-250:],flush=True)
        bits=sbits()
        ok(bits==0 and not is_sulk(t),'a normal win (no CURSE): no sulk bit, the usual text')
    elif MY=='kill':
        i,t=first_trainer(MAP,SPR)
        fight()
        for k in range(10):press_('b',60)
        bits=sbits()
        ok(m[0xd453]==1 and bits==0,'killed with CURSE: murder, no sulk bit')
print('t77 done',flush=True)
