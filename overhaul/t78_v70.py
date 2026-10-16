# v70: killed scripted grunts don't talk after the battle (NUGGET BRIDGE Rocket, CERULEAN thief); flags/world change still happen; alive = the usual text
import sys
MY=sys.argv[1]
sys.argv=['x','none']
src=open('t28_v14.py').read().split("if MODE=='mirage_rate':")[0].replace("MODE=sys.argv[1]","MODE='x'")
exec(src)
def ok(c,msg):print(('PASS ' if c else 'FAIL ')+msg,flush=True)
def tog(n):return (m[0xd5a6+n//8]>>(n%8))&1       # 1 = hidden
def run_script(var,val,frames=700):
    m[var]=val;m[0xda39]=val;seen.clear()
    for i in range(frames//10):
        T(10)
        if m[var]==0:break
    for i in range(40):
        if m[var]==0 and not box():break
        press_('a',60)
    return allt().replace("'","")
if MY=='route24':
    for killed in (False,True):
        warp_from_pallet(0x23,0);m[0xd887]=0;m[0xd7ef]|=1        # the NUGGET was given (bit 0)
        m[0xd7ef]&=~2
        if killed:m[0xd44f]|=0x20
        m[0xd057]=0
        t=run_script(0xd602,3)
        print('killed' if killed else 'alive','text:',t[-200:],'| d7ef',hex(m[0xd7ef]),flush=True)
        ok(m[0xd7ef]&2==2,'%s: EVENT_BEAT_ROUTE24_ROCKET (D7EF bit 1) is set'%('killed' if killed else 'alive'))
        ok(m[0xd602]==0,'%s: the map script is finished'%('killed' if killed else 'alive'))
        if killed:ok(sum(c.isalpha() for c in t)<3,'killed: no dialogue')
        else:ok(len(t.strip())>10,'alive: his usual after-battle text is shown')
elif MY=='cerulean':
    for killed in (False,True):
        warp_from_pallet(0x03,0);m[0xd887]=0
        m[0xd75b]&=~0x80
        if killed:m[0xd44f]|=0x10
        m[0xd057]=0
        before=(tog(7),tog(9),tog(6))
        t=run_script(0xd60f,4,1400)
        after=(tog(7),tog(9),tog(6))
        k='killed' if killed else 'alive'
        print(k,'text:',t[-200:],'| toggles',before,'->',after,'d75b',hex(m[0xd75b]),flush=True)
        ok(m[0xd75b]&0x80,'%s: EVENT_BEAT_CERULEAN_ROCKET_THIEF (D75B bit 7) is set'%k)
        ok(m[0xd60f]==0,'%s: the map script is finished'%k)
        if killed:
            ok(sum(c.isalpha() for c in t)<3,'killed: no dialogue')
            ok(after[0]==0 and after[1]==1 and after[2]==1,'killed: the event\'s world change happened (object 7 shown, 9 and 6 hidden)')
        else:
            ok(len(t.strip())>10,'alive: his usual speech is shown')
            ok(after[0]==0 and after[1]==1 and after[2]==1,'alive: the same world change')
print('t78 done',flush=True)
