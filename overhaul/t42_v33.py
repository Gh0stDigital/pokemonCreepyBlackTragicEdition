# v33: PRETA's back picture shaded like the front: black outline unchanged, only body whites turned grey (dark + light),
# the background and the thin bands stay white, compressed picture still fits its slot.
import sys,json
from harness import ROM
import preta_back as P
def ok(c,msg):
    print(('PASS ' if c else 'FAIL ')+msg,flush=True)
    if not c:sys.exit(1)
new=P.load(ROM);old=P.load(ROM.replace('v33','v32'))
diff=[(y,x) for y in range(32) for x in range(32) if new[y][x]!=old[y][x]]
ok(all(old[y][x]==0 and new[y][x] in (1,2) for y,x in diff),'%d body pixels white -> grey, nothing else changed'%len(diff))
bg=P.outside(old)
ok(not any(bg[y][x] for y,x in diff),'the background around PRETA stays white')
from collections import Counter
c=Counter(v for row in new for v in row)
ok(c[2]>0 and c[1]>c[2],'dark and light grey both used, light more than dark (like the front): light %d, dark %d'%(c[1],c[2]))
ok(json.load(open('manifest_v33.json'))['preta_back']['bytes']<=191,'fits the original slot')
print('v33 back: ALL PASS')
