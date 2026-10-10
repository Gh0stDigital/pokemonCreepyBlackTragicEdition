# Trainer headers in the ROM and the map each header list belongs to (for the v29 kill system).
# A header is 12 bytes: flag bit (= the trainer's sprite index), range<<4, flag address (D747-D886), 4 text pointers;
# the base hack reuses the 4th pointer (offset 0xA) as the kill index (only 23 trainers got one).
from patchguard import fo
def headers(r):
    w=lambda o:r[o]|r[o+1]<<8;hs=[]
    for o in range(0x4000,len(r)-12):
        if o%0x4000>0x3ff4:continue
        b,rng=r[o],r[o+1]
        if b>15 or rng&15 or rng>0x90:continue
        if not 0xd747<=w(o+2)<0xd887:continue
        if not all(0x4000<=w(o+k)<0x8000 for k in (4,6,8)):continue
        hs.append(o)
    return hs
def groups(r,hs):
    s=set(hs);return sorted(o for o in hs if o-12 not in s)
def map_header(r,mp):
    bank=r[0xc23d+mp];h=r[0x1ae+2*mp]|r[0x1ae+2*mp+1]<<8;return bank,fo(bank,h)
def group_maps(r,hs):
    """group start -> map id: the map whose script starts closest before the code that loads the group (ld hl,<group>)"""
    scripts={}
    for mp in range(0xf8):
        bank,h=map_header(r,mp)
        if 1<=bank<=0x3f:scripts.setdefault(bank,[]).append((r[h+7]|r[h+8]<<8,mp))
    out={}
    for g in groups(r,hs):
        b=g//0x4000;a=0x4000+g%0x4000;pat=bytes([0x21,a&255,a>>8])
        refs=[0x4000+o%0x4000 for o in range(b*0x4000,b*0x4000+0x4000) if r[o:o+3]==pat]
        owners=set()
        for ra in refs:
            cand=[(sp,mp) for sp,mp in scripts.get(b,[]) if sp<=ra]
            if cand:owners.add(max(cand)[1])
        out[g]=sorted(owners)
    return out
if __name__=='__main__':
    import sys
    r=open(sys.argv[1],'rb').read();hs=headers(r);gm=group_maps(r,hs)
    print(len(hs),'headers',len(gm),'groups; unmapped',[hex(g) for g,v in gm.items() if not v],'multi',{hex(g):v for g,v in gm.items() if len(v)>1})
def header_maps(r,hs,maxtext=40):
    """header file offset -> map id, from the maps' text tables: a trainer's text is TX_ASM 'ld hl,<header>; call ...'"""
    S=set(hs);out={}
    for mp in range(0xf8):
        bank,h=map_header(r,mp)
        if not 1<=bank<=0x3f:continue
        tp=r[h+5]|r[h+6]<<8
        if not 0x4000<=tp<0x8000:continue
        for i in range(maxtext):
            o=fo(bank,tp)+2*i;p=r[o]|r[o+1]<<8
            if not 0x4000<=p<0x8000:break
            t=fo(bank,p)
            if r[t]==0x08 and r[t+1]==0x21:
                ho=fo(bank,r[t+2]|r[t+3]<<8)
                if ho in S:out.setdefault(ho,set()).add(mp)
    return out
