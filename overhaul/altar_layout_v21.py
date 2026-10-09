# v21 TOWER CHAMBER: v20's round room, plus a thin ring of the purification pattern around the single centre tile and a
# triangle of three POKeMON statues around it, each with a gravestone in front (the tile below it). The four diagonal
# shrines are gone (the triangle replaces them). Same 24x24 steps / 12x12 blocks, stairs and centre as v20.
import math
from altar_layout_v20 import STEP_TILES,W_BLK,H_BLK,CY,CX,STAIRS_STEP,MU_STEP,blocks
def steps():
    g=[]
    for y in range(2*H_BLK):
        row=[]
        for x in range(2*W_BLK):
            d=math.hypot(y-CY,x-CX)
            row.append('C' if d==0 or 1.8<=d<=2.4 else 'F' if d<=7.4 else 'G' if d<=9.4 else 'W')
        g.append(row)
    g[19][CX]='S';g[18][CX]='F'
    for x in (CX-1,CX+1):g[17][x]='U';g[18][x]='L'                 # statues by the stairs (as v20)
    for y,x in ((5,CX),(13,CX-5),(13,CX+5)):                       # triangle around the centre (point up)
        g[y][x]='U';g[y+1][x]='L';g[y+2][x]='G'                     # statue, gravestone in front of it
    return g
