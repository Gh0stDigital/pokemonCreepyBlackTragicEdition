# v19 secret room behind AGATHA on Pokemon Tower 7F: a round chamber (Pokemon Tower tileset 0F), 11x11 blocks.
import math
W=H=11;C=5
WALL,FLOOR,GRAVES,CENTER,STAIRS,STATUE_L,STATUE_R,SHRINE_R,SHRINE_L=0x01,0x0e,0x02,0x33,0x31,0x45,0x4b,0x13,0x17
def layout():
    rows=[]
    for y in range(H):
        row=[]
        for x in range(W):
            d=math.hypot(x-C,y-C)
            if d<0.5:b=CENTER                       # the circle's centre: purification-circle pattern, MR. MU stands here
            elif d<=3.2:b=FLOOR
            elif d<=4.3:b=GRAVES                    # a ring of graves around the chamber
            else:b=WALL
            row.append(b)
        rows.append(row)
    rows[9][C]=STAIRS                               # way back down (stairs in the block's top-right step)
    rows[8][C-1]=STATUE_R;rows[8][C+1]=STATUE_L     # two statues flank the entrance
    for y,x,b in ((3,3,SHRINE_R),(3,7,SHRINE_L),(7,3,SHRINE_R),(7,7,SHRINE_L)):rows[y][x]=b   # four small shrines on the diagonals
    return rows
STAIRS_STEP=(18,11)                                 # warp: top-right step of the stairs block
MU_STEP=(10,10)                                     # top-left step of the centre block
