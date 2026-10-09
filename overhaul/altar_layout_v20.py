# v20 TOWER CHAMBER drawn per walking tile (step), so the circle has ONE centre tile. 24x24 steps = 12x12 blocks.
# Each block is built from four 2x2-tile quarters; combinations the Tower blockset lacks get new block ids in its
# unused slots (6E-AF, not referenced by any map using tileset 0F).
import math
W_BLK=H_BLK=12;CY=CX=11                              # centre step
STEP_TILES={'W':(0x11,0x11,0x11,0x11),             # wall
            'F':(0x01,0x01,0x01,0x01),             # stone floor
            'G':(0x09,0x0a,0x19,0x1a),             # grave
            'C':(0x22,0x22,0x22,0x22),             # the centre: one purification-circle tile
            'S':(0x0b,0x0c,0x1b,0x1c),             # stairs down
            'H':(0x05,0x06,0x15,0x16),             # small shrine
            'U':(0x01,0x01,0x27,0x2f),             # statue (top)
            'L':(0x37,0x3f,0x3d,0x3e)}             # statue (bottom)
def steps():
    g=[]
    for y in range(2*H_BLK):
        row=[]
        for x in range(2*W_BLK):
            d=math.hypot(y-CY,x-CX)
            row.append('C' if d==0 else 'F' if d<=7.4 else 'G' if d<=9.4 else 'W')
        g.append(row)
    for y,x in ((7,7),(7,15),(15,7),(15,15)):g[y][x]='H'          # four shrines on the diagonals
    g[19][CX]='S';g[18][CX]='F'                                    # stairs (and the step in front of them)
    for x in (CX-1,CX+1):g[17][x]='U';g[18][x]='L'                 # statues on both sides of the way in
    return g
STAIRS_STEP=(19,CX);MU_STEP=(CY,CX)
def blocks(g):
    """-> rows of 16-byte block definitions"""
    out=[]
    for by in range(H_BLK):
        row=[]
        for bx in range(W_BLK):
            t=[0]*16
            for qy in (0,1):
                for qx in (0,1):
                    a,b,c,d=STEP_TILES[g[2*by+qy][2*bx+qx]]
                    t[(2*qy)*4+2*qx]=a;t[(2*qy)*4+2*qx+1]=b;t[(2*qy+1)*4+2*qx]=c;t[(2*qy+1)*4+2*qx+1]=d
            row.append(bytes(t))
        out.append(row)
    return out
