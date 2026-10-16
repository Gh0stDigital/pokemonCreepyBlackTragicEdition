# Static check of the outdoor sprite sets: every object picture of every outdoor map must be in the set(s) the map can use (also the ones chosen by position
# for routes, 5:7A89), compared with the baseline ROM (v62: the violations that already existed). Towns with a shamaness must have picture 19 in their set.
# usage: python3 check_sets.py [ROM] [BASELINE_ROM]
import sys
import town_map as T
def load(path):
    T.R=open(path,'rb').read();R=T.R
    tab=R[T.fo(5,0x7a64):T.fo(5,0x7a64)+0x25];spec=R[T.fo(5,0x7a89):T.fo(5,0x7ab9)]
    def sets_of(s):
        if s<0xf0:return [s]
        e=spec[((s&0x0f)-1)*4:((s&0x0f)-1)*4+4];return [e[2],e[3]]
    def data(s):
        if s==13 and R[T.fo(5,0x7a64)+2]==13:return list(R[T.fo(5,0x7f79):T.fo(5,0x7f79)+11])
        o=T.fo(5,0x7ab9)+(s-1)*11;return list(R[o:o+11])
    viol=set();info={}
    for mid in range(0x25):
        try:d=T.info(mid)
        except Exception:continue
        pics={o[0] for o in d['objs']}
        for s in sets_of(tab[mid]):
            S=data(s);info[(mid,s)]=S
            for pc in pics:
                if pc and pc not in S:viol.add((mid,s,pc))
    return viol,info
rom=sys.argv[1] if len(sys.argv)>1 else 'Creepy_Black_Mu_v66.gb'
base=sys.argv[2] if len(sys.argv)>2 else 'Creepy_Black_Mu_v62.gb'
vb,_=load(base);vn,info=load(rom)
new=sorted(vn-vb)
print('baseline violations',len(vb),'now',len(vn))
for v in new:print('NEW VIOLATION: map %02x set %d picture %02x'%v)
miss=[mid for mid in (0,1,2,3,4,5,6,7,8,0x0a) if not any(0x19 in S for (m_,s),S in info.items() if m_==mid)]
for mid in miss:print('NO CHANNELER PICTURE in the set of map %02x'%mid)
print('OK' if not new and not miss else 'FAIL')
sys.exit(1 if new or miss else 0)
