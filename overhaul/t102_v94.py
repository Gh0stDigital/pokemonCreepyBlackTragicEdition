# v94: the climax evolution scene is RED -> BLACK only (no GHOST picture).  Mode: evo (t85's climax run with a hook on the evolution's picture loader)
import sys
sys.argv=['x','climax']
s=open('t85_v77.py').read()
s=s.replace("snd=[]\n","snd=[]\npics=[]\np.hook_register(0x1e,0x7f04,lambda c:pics.append(m[0xd0b5]),None)\n",1)
i=s.rindex("print('t85 done',flush=True)")
s=s[:i]+"seq=[x for k,x in enumerate(pics) if k==0 or pics[k-1]!=x]\nprint('evolution pictures',[hex(x) for x in pics],flush=True)\nok(0x86 in pics and 0x7f in pics and 0x1f not in pics and pics.index(0x86)<pics.index(0x7f),'the scene shows RED, then BLACK - no GHOST picture (%s)'%[hex(x) for x in seq])\nok(m[0xd46c]==1 and m[RIT]==6 and 0x1f not in party() and party()[0]==0x7f,'BLACK is born and GHOST is not in the party')\n"
exec(compile(s.replace("MY85=sys.argv[1]","MY85='climax'"),'t85mod','exec'))
