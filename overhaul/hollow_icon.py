# Party-menu icon for ????? (the MIRAGE): the GENTLEMAN overworld sprite hollowed out (outline only).
# A Gen 1 party icon is the LEFT half (8x16) drawn twice, the right copy mirrored by the hardware: 2 tiles per frame
# (top, bottom), 2 frames (the second one is shifted down 1 pixel: the bobbing animation).
import sys
def fo(b,a):return b*0x4000+a-0x4000
def gentleman_frame(r,f=0):
    T=fo(5,0x7b27)                                           # sprite sheet pointer table (entries: ptr, size, bank)
    e=T+0x7b3d-0x7b27+4*(0x10-1) if False else None
    i=r.find(bytes.fromhex('8041c005'));e=i+4*(0x10-1);ptr=r[e]|r[e+1]<<8;bank=r[e+3];o=fo(bank,ptr)
    g=[[0]*16 for _ in range(16)]
    for t,(ty,tx) in enumerate(((0,0),(0,1),(1,0),(1,1))):
        b=r[o+(f*4+t)*16:o+(f*4+t)*16+16]
        for y in range(8):
            lo,hi=b[2*y],b[2*y+1]
            for x in range(8):g[ty*8+y][tx*8+x]=((lo>>(7-x))&1)|(((hi>>(7-x))&1)<<1)
    return g
def hollow_left(r):
    g=gentleman_frame(r,0)
    black=lambda y,x:0<=y<16 and 0<=x<16 and g[y][x]==3
    out=[[0]*8 for _ in range(16)]
    for y in range(16):
        for x in range(8):
            if g[y][x]==3 and not all(black(y+dy,x+dx) for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))):out[y][x]=3
            elif g[y][x]==2:out[y][x]=2                      # keep the hat band's grey
    return out
def frames(r):
    a=hollow_left(r)
    b=[[0]*8]+[row[:] for row in a[:-1]]                     # frame 2: one pixel lower
    return a,b
def tile_bytes(left,y0):                                     # 8x8 tile of the left half starting at row y0 -> 16 bytes
    out=bytearray()
    for y in range(y0,y0+8):
        lo=hi=0
        for x in range(8):c=left[y][x];lo=lo<<1|(c&1);hi=hi<<1|(c>>1)
        out+=bytes([lo,hi])
    return bytes(out)
def four_tiles(r):
    a,b=frames(r);return [tile_bytes(a,0),tile_bytes(a,8),tile_bytes(b,0),tile_bytes(b,8)]   # top1,bot1,top2,bot2
def preview(r,scale=10):
    from PIL import Image
    a,b=frames(r);im=Image.new('RGB',(2*(16*scale+30),16*scale),(255,255,255))
    pal={0:None,1:(255,255,255),2:(170,170,170),3:(0,0,0)}
    for k,left in enumerate((a,b)):
        for y in range(16):
            for x in range(16):
                c=left[y][x if x<8 else 15-x]
                if c:
                    for dy in range(scale):
                        for dx in range(scale):im.putpixel((k*(16*scale+30)+x*scale+dx,y*scale+dy),pal[c])
    return im
if __name__=='__main__':
    r=open(sys.argv[1],'rb').read();preview(r).save(sys.argv[2])
