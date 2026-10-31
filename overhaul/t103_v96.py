# v96: VICTORY ROAD: no gravestone as a third four-tile picture (item ball / boulder keep their own VRAM slots; the killed trainer stays hidden);
#      MT. MOON (only item balls) still gets gravestones (control).  BLUE (Champion) plays the victory music again; LORELEI stays silent (control).
#  Modes: vr, blue
import sys
MY103=sys.argv[1]
def ok(c,msg):
    print(('PASS ' if c else 'FAIL ')+msg,flush=True)
    if not c:sys.exit(1)
if MY103=='vr':
    sys.argv=['x','none']
    exec(open('t36_v28.py').read().split("if MODE=='panic':")[0])
    ROMB=open(os.environ['CB_ROM'],'rb').read()
    fo=lambda b,a:b*0x4000+a-0x4000
    def tbl(mp):
        o=fo(0x2d,0x7180)+2*mp;ptr=ROMB[o]|ROMB[o+1]<<8;q=fo(0x2d,ptr);out=[]
        while ROMB[q]:out.append((ROMB[q],ROMB[q+1]|ROMB[q+2]<<8));q+=3
        return out
    def visit(mp):
        t=tbl(mp)
        load('pallet_with_ghost');m[0xd455]=255
        for s,k in t[:2]:
            base=0xd430 if k>=0x100 else 0xd4a4;kk=k&0xff;m[base+kk//8]|=1<<(kk%8)
        for i in range(m[0xd3ae]):m[0xd3af+4*i+2]=0;m[0xd3af+4*i+3]=mp
        for i in range(6):
            if m[0xd35e]==mp:break
            p.button('up',8);T(24)
        T(120);return [s for s,k in t[:2]]
    def slots(pc):return {m[0xc102+16*i]>>4 for i in range(1,m[0xd4e1]+1) if m[0xc100+16*i]==pc and m[0xc102+16*i]!=0xff}
    killed=visit(0xc6)
    pics=[m[0xc100+16*i] for i in range(1,m[0xd4e1]+1)]
    print('VICTORY ROAD 3F pictures',[hex(x) for x in pics],'ball slots',slots(0x3d),'boulder slots',slots(0x3f))
    ok(0x49 not in pics,'VICTORY ROAD 3F (item balls + boulders): killed trainers get no gravestone picture')
    ok(slots(0x3d) and slots(0x3f) and not (slots(0x3d)&slots(0x3f)),'the item ball and the boulder use different VRAM slots')
    hid={}
    p.hook_register(0x2d,0x6248,lambda c:hid.__setitem__(m[0xffda]>>4,p.register_file.A),None)
    T(60)
    print('predef 0x13 results per object',hid)
    ok(all(hid.get(i)==1 for i in killed),'the killed trainers are hidden every frame (predef 0x13 -> 1)')
    ok(all(hid.get(i)==0 for i in (3,4) if i in hid),'the living trainers are drawn (control)')
    visit(0x3b);pics=[m[0xc100+16*i] for i in range(1,m[0xd4e1]+1)]
    ok(pics.count(0x49)==2,'MT. MOON 1F (item balls only): the killed trainers are gravestones as before (control)')
elif MY103=='blue':
    ids=[]
    s=open('t94_v86.py').read()
    sys.argv=['x','hof']
    s=s.replace("MY94=sys.argv[1]","MY94='hof'")
    s=s.replace("    src66=open('t66_v58.py').read()","    p.hook_register(0,0x23de,lambda c:ids.append((p.register_file.A,m[0xd031],m[0xd057])),None)\n    src66=open('t66_v58.py').read()",1)
    s=s.replace("    pics=[]\n","    bl=sorted({hex(a) for a,c,b in ids if c==0x2b});print('ids in BLUE battle',bl,flush=True)\n    ok(any(a in (0xf6,0xf9,0xfc) and c==0x2b for a,c,b in ids),'BLUE (the Champion) plays the victory music')\n    pics=[]\n",1)
    exec(compile(s,'t94mod','exec'))
