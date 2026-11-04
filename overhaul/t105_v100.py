# v100: the consort needs BADGES (ERIKA 4, MISTY 6, SABRINA 8). Mode = MISTY / ERIKA / SABRINA.
# For each girl, in her gym after beating her, AGATHA stage 4, HELIX FOSSIL in the bag, YES to "Give <NAME> the HELIX FOSSIL?":
#  one BADGE short -> her refusal ("can't just be seen with anyone", "strong trainer"), shell kept, stage 4, no consort
#  enough BADGES  -> her v16 reply, shell taken, stage 5, consort set (control)
import sys
MY=sys.argv[1]
sys.argv=['x','none']
exec(open('t28_v14.py').read().split("if MODE=='mirage_rate':")[0].replace("MODE=sys.argv[1]","MODE='x'"))
def ok(c,msg):print(('PASS ' if c else 'FAIL ')+msg,flush=True)
GIRLS={'MISTY':(1,0x41,(0xd75e,7),6,'For me?'),'ERIKA':(2,0x86,(0xd77c,1),4,'A gift for me?'),'SABRINA':(3,0xb2,(0xd7b3,1),8,'I knew')}
n,mp,beat,need,join=GIRLS[MY]
def summon(i):
    y,x=m[0xd361],m[0xd362];b1=0xc100+i*16;b2=0xc200+i*16
    m[b1+4]=0x2c;m[b1+6]=0x40;m[b1+2]=1 if m[b1+2]==0xff else m[b1+2];m[b2+4]=y-1+4;m[b2+5]=x+4;m[b2+6]=0xff
def talk_up(i,n=40):
    summon(i);T(10);p.button('up',8);T(20);seen.clear()
    for k in range(n):
        if m[0xd057] or (not box() and k>12):break
        press_('a',70)
    return allt().replace("'","")
def helix():return any(m[0xd31e+2*k]==0x2a for k in range(m[0xd31d]))
def run(badges):
    warp_from_pallet(mp,0)
    m[0xd464]=4;m[0xd465]=0;m[beat[0]]|=1<<beat[1];m[0xd356]=(1<<badges)-1 if badges<8 else 0xff
    k=m[0xd31d];m[0xd31e+2*k]=0x2a;m[0xd31e+2*k+1]=1;m[0xd31e+2*k+2]=0xff;m[0xd31d]=k+1
    T(10);t=talk_up(1);print(t[-500:],flush=True);return t
t=run(need-1)
ok('HELIX FOSSIL?' in t,'%s: the question "Give %s the HELIX FOSSIL?"'%(MY,MY))
ok('just be seen' in t or 'with just' in t,'%s with %d BADGES: she refuses (not with just anyone)'%(MY,need-1))
ok('strong' in t and 'BADGES' in t,'... only a strong trainer, come back with the BADGES')
ok(join not in t,'... no join reply')
ok(helix() and m[0xd464]==4 and m[0xd465]==0,'... shell kept, stage 4, no consort (D464 %d D465 %d)'%(m[0xd464],m[0xd465]))
t=run(need)
ok(join in t and 'just be seen' not in t and 'with just' not in t,'%s with %d BADGES: her usual reply (control)'%(MY,need))
ok(not helix() and m[0xd464]==5 and m[0xd465]==n,'... she took the shell, stage 5, consort %d'%m[0xd465])
