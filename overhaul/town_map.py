# ASCII view of a town map: passable steps, warps, objects, signs (used to place the v63 shamanesses)
import sys
R=open('Creepy_Black_Mu_v62.gb','rb').read()
w=lambda a:R[a]|R[a+1]<<8
fo=lambda b,a:b*0x4000+a-0x4000
def info(mid):
    h=w(0x1ae+2*mid);b=R[0xc23d+mid];o=fo(b,h)
    ts,H,W=R[o],R[o+1],R[o+2];blk=w(o+3);txt=w(o+5);scr=w(o+7);conn=R[o+9]
    n=bin(conn&15).count('1');objp=w(o+10+11*n)
    # blocks
    bo=fo(b,blk);blocks=[R[bo+i] for i in range(W*H)]
    # tileset
    t=fo(3,0x47be)+12*ts;tb=R[t];bs=w(t+1);cl=w(t+5)
    co=cl  # collision list in home bank
    passable=set()
    i=co
    while R[i]!=0xff:passable.add(R[i]);i+=1
    bso=fo(tb,bs)
    objo=fo(b,objp)
    p=objo+1;nw=R[p];p+=1;warps=[(R[p+4*i],R[p+4*i+1]) for i in range(nw)];p+=4*nw
    ns=R[p];p+=1;signs=[(R[p+3*i],R[p+3*i+1]) for i in range(ns)];p+=3*ns
    no=R[p];p+=1;objs=[]
    for i in range(no):
        t_=R[p+5];sz=6+(2 if t_&0x40 else 0)+(1 if t_&0x80 else 0)
        objs.append((R[p],R[p+1]-4,R[p+2]-4,t_));p+=sz
    return dict(ts=ts,H=H,W=W,blocks=blocks,bs=bso,passable=passable,warps=warps,signs=signs,objs=objs,bank=b,hdr=h,txt=txt,scr=scr,conn=conn)
def grid(mid):
    d=info(mid);H,W=d['H'],d['W'];g=[]
    for sy in range(2*H):
        row=''
        for sx in range(2*W):
            bid=d['blocks'][(sy//2)*W+sx//2]
            tile=d['bs'] and R[d['bs']+16*bid+(2*(sy%2)+1)*4+2*(sx%2)]
            row+='.' if tile in d['passable'] else '#'
        g.append(list(row))
    for (y,x) in d['warps']:
        if 0<=y<2*H and 0<=x<2*W:g[y][x]='W'
    for (y,x) in d['signs']:
        if 0<=y<2*H and 0<=x<2*W:g[y][x]='S'
    for pic,y,x,t in d['objs']:
        if 0<=y<2*H and 0<=x<2*W:g[y][x]='O'
    return d,[''.join(r) for r in g]
if __name__=='__main__':
    for mid in map(lambda s:int(s,0),sys.argv[1:]):
        d,g=grid(mid)
        print('map',hex(mid),'bank',hex(d['bank']),'size',d['W']*2,'x',d['H']*2,'objs',len(d['objs']),'pics',[hex(o[0]) for o in d['objs']])
        print('    '+''.join(str(x%10) for x in range(2*d['W'])))
        for y,r in enumerate(g):print('%3d %s'%(y,r))
