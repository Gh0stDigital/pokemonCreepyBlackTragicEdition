from pathlib import Path
import re,json,hashlib
ROOT=Path(__file__).resolve().parent.parent
base=(ROOT/'original/base/Pokemon_Black_(Creepy)_d.gb').read_bytes();r=bytearray(base);log=[]
def patch(o,data,name,old=None):
 data=bytes(data)
 if old is not None: assert r[o:o+len(bytes.fromhex(old))]==bytes.fromhex(old),(name,hex(o))
 log.append(dict(offset=hex(o),before=r[o:o+len(data)].hex(),after=data.hex(),name=name));r[o:o+len(data)]=data
class Code:
 def __init__(self,org):self.org=org;self.b=bytearray();self.labels={};self.refs=[]
 def emit(self,h):self.b+=bytes.fromhex(h)
 def raw(self,b):self.b+=b
 def word(self,n):self.b+=int(n).to_bytes(2,'little')
 def label(self,n):self.labels[n]=self.org+len(self.b)
 def ref(self,op,n):self.emit(op);self.refs.append((len(self.b),n));self.word(0)
 def finish(self):
  for p,n in self.refs:self.b[p:p+2]=self.labels[n].to_bytes(2,'little')
  return self.b
cm={k:int(v,16) for k,v in re.findall(r'^charmap "([^"]+)", \$([0-9A-Fa-f]+)',(ROOT/'pokeblack/charmap.asm').read_text(),re.M)}
def enc(s):
 out=bytearray()
 while s:
  k=next(k for k in sorted(cm,key=len,reverse=True) if s.startswith(k));out.append(cm[k]);s=s[len(k):]
 return out
def txt(paras,end=0x58):
 out=bytearray([0])
 for i,p in enumerate(paras):
  if i:out.append(0x51)
  for j,line in enumerate(p):
   assert len(line)<=18,line
   if j:out.append(0x4f if j==1 else 0x55)
   out+=enc(line)
 out.append(end);return out
def far(addr,bank):return b'\x21'+addr.to_bytes(2,'little')+bytes([6,bank,0xcd,0x18,0x36])
def jp(addr):return b'\xc3'+addr.to_bytes(2,'little')
# Saved spare bytes: d450 answer(1 trainer,2 Pokemon), d451 awarded Ghost,
# d452 used Curse this battle, d453 killed a trainer, d454 Mu state(0/1/2/3).
# Bank 6 free space contains Pallet data and local script.
c=Code(0x6800)
dialogue={
'oak':[ ['Hello there!','Welcome to the','world of #MON!'],['My name is OAK!','People call me','the #MON PROF!'],['I am hiring you','as a research','agent.']],
'briefing':[['<PLAYER>!'],['Some people use','#MON as weapons','to commit crimes','and even murder.'],['They hurt others','to get what','they want.'],['The law permits','#MON to be used','in self-defense','only.'],['Be careful in','this region.'],['Your research','journey is about','to begin!']],
'mu_question':[['I am MR. MU.'],['If a #MON kills','a person while','obeying its','TRAINER...'],['Who is','responsible?']],
'menu':[[' THE TRAINER',' THE POKéMON']],
'mu_after':[['I see.'],['Remember your','answer.']],
'shaman':[['Long before the','LEAGUE, there were','people in KANTO'],['who worshiped an','old god of','the dead.'],['They believed the','souls of humans','could be caught...'],['bound...','and commanded.'],['Like #MON.'],['Those who','practiced it were','said to carry'],['the dead with','them as servants.'],['...'],['But the old','stories say that','once you begin'],['playing with','souls...'],['...something','eventually begins','playing with','yours.']],
'ghost_notice':[['A cold presence','follows you...'],['GHOST joined','your party!']],
'fear0':[['Wh-what did you','do to my #MON!?'],['Please...','spare my life!']],
'fear1':[['What is that','monster!?'],['Keep it away','from me!']],
'fear2':[['My #MON...','What have you','done!?'],["Don't let it",'take me too!']],
'police':[['Be on the lookout','for a criminal','TRAINER.'],['Reports describe','attacks that kill','both people and','#MON.'],['Some witnesses','blame TEAM ROCKET.'],['Others describe','a lone TRAINER.'],['The reports are','conflicting.','Stay alert!']]
}
for k,v in dialogue.items():
 c.label(k);c.raw(txt(v,0x57 if k in ('menu','briefing') else 0x58))
# new object table: preserve original objects/signs and append NPCs before warp-to.
c.label('objects');obj=bytearray(base[0x182c3:0x182fd]);assert obj[27]==3
obj[27]=5;obj=obj[:46]+bytes([0x25,10,12,0xff,0xd2,8,0x28,19,13,0xff,0xd1,9])+obj[46:];c.raw(obj)
c.label('texttable');c.raw(base[0x18f88:0x18f96]);c.ref('', 'mu_text');c.ref('','shaman')
c.label('move');c.raw(bytes([0x80,0x80,0xff]))
# Called every Pallet frame instead of original entry. Never disturb Oak's script.
c.label('pallet');c.emit('fa 51 d4 a7');c.ref('ca','mu_check');c.emit('af ea 50 c1 3e ff ea 54 c2 ea 55 c2')
c.label('mu_check');c.emit('fa 54 d4 fe 03');c.ref('ca','hide_mu');c.emit('fe 02');c.ref('ca','original');c.emit('fe 01');c.ref('ca','wait_mu')
# Trigger on first exit; player initially at x5 y6. Freeze input and walk Mu from x8 to6.
c.emit('fa 61 d3 fe 06');c.ref('c2','original');c.emit('fa 62 d3 fe 05');c.ref('c2','original');c.emit('3e 01 ea 54 d4 3e ff ea 6b cd 3e 04 e0 8c');c.ref('11','move');c.emit('cd 74 36 c9')
c.label('wait_mu');c.emit('fa 30 d7 cb 47 c0 cd 87 3c 3e 04 e0 8c cd 4d 29 3e 02 ea 54 d4 af ea 6b cd c9')
c.label('hide_mu');c.emit('af ea 40 c1 3e ff ea 44 c2 ea 45 c2')
c.label('original');c.emit('fa 4b d7 cb 67 c3 60 4e')
# Interactive choice: original game's cursor/input routine, exact choice labels.
c.label('mu_text');c.emit('08 fa 50 d4 a7');c.ref('c2','mu_repeat');c.ref('21','mu_question');c.emit('cd 94 3c');c.ref('21','menu');c.emit('cd 94 3c af ea 26 cc ea 2a cc ea 35 cc ea 37 cc ea 4a cc 3e 0e ea 24 cc 3e 01 ea 25 cc ea 28 cc ea 29 cc f0 f6 cb 8f e0 f6 cd f2 3a fa 26 cc 3c ea 50 d4')
c.label('mu_repeat');c.ref('21','mu_after');c.emit('cd 94 3c c3 04 25')
code6=c.finish();assert 0x6800+len(code6)<0x8000
patch(0x1a800,code6,'Pallet events, NPC objects, dialogue')
patch(0x182c1,c.labels['objects'].to_bytes(2,'little'),'Pallet object pointer','c342')
patch(0x182a6,c.labels['texttable'].to_bytes(2,'little'),'Pallet text pointer','884f')
patch(0x18e5b,jp(c.labels['pallet'])+b'\0\0','Pallet script hook','fa4bd7cb67')
# Oak wrappers only. Preserve Oak, demonstration species, Red and rival graphics.
for o,k in [(0x622c,'oak'),(0x6245,'briefing')]:patch(o,b'\x17'+c.labels[k].to_bytes(2,'little')+b'\x06\x50','Oak '+k)
# Global helpers, empty bank 2e.
g=Code(0x4000)
g.label('mapload');g.emit('fa 54 d4 fe 02 c0 fa 5e d3 a7 c8 3e 03 ea 54 d4 c9')
g.label('award');g.emit('fa 50 d4 fe 01 c0 fa 51 d4 a7 c0 3e 01 ea 27 d1 3e 1f ea 91 cf ea 1e d1 cd 5b 39 3e 01 ea 51 d4 c9')
g.label('fear');g.emit('fa 52 d4 a7 c8 3e 06 ea 92 d0 fa 31 d0 e6 03 fe 03');g.ref('c2','fearchoose');g.emit('af');g.label('fearchoose');g.emit('87 5f 16 00');g.ref('21','fears');g.emit('19 2a ea 8d d0 ea 8f d0 7e ea 8c d0 ea 8e d0 c9')
g.label('fears');[g.word(c.labels['fear'+str(i)]) for i in range(3)]
# Preserve ordinary dialogue and guard progression; add bulletin to guards after a murder.
g.label('police');g.emit('fa 3c cc a7 c0 fa 47 cc a7 c0 fa 53 d4 a7');g.ref('ca','waittext');g.emit('fa 13 cf a7');g.ref('ca','waittext');g.emit('47 fa e1 d4 b8');g.ref('da','waittext');g.emit('78 cb 37 6f 26 c1 7e fe 31');g.ref('ca','alert');g.emit('fe 32');g.ref('c2','waittext');g.label('alert');g.emit('cd 99 38');g.raw(far(c.labels['police'],6)) # data not executable! use fartext wrapper below
# replace above call target with bank46 local wrapper PrintText of TX_FAR.
g.b=g.b[:-8];g.ref('21','police_far');g.emit('cd 94 3c');g.label('waittext');g.emit('c3 99 38');g.label('police_far');g.emit('17');g.word(c.labels['police']);g.emit('06 50')
patch(0xb8000,g.finish(),'Saved event and dialogue helpers')
# bank3 stub for map lifecycle; original roster loading preserved.
s=Code(0x7f80);s.label('map');s.raw(far(g.labels['mapload'],46));s.emit('21 a2 4e c3 2d 4e')
s.label('kill');s.emit('3e 01 ea 53 d4 21 a4 d4 c9')
patch(0xff80,s.finish(),'Map-exit and trainer-death hooks')
patch(0xce2a,jp(s.labels['map']),'Track leaving Pallet','21a24e')
patch(0xcd99,b'\xcd'+s.labels['kill'].to_bytes(2,'little'),'Record actual trainer murder','21a4d4')
# Bank7 after first rival battle: keep heal/event then add Ghost.
a=Code(0x7000);a.raw(far(g.labels['award'],46));a.emit('21 4b d7 cb de c9')
patch(0x1f000,a.finish(),'Award Ghost after rival battle')
patch(0x1ce27,bytes.fromhex('cd 00 70 00 00'),'Post-rival award hook','214bd7cbde')
patch(0x1d210,bytes(16),'Remove pre-battle Ghost award','3e01ea27d13e1fea91cfea1ed1cd5b39')
# Battle init stub in bank14 free area (inspect/allocate actual trailing zero area).
bank=0x14;end=(bank+1)*0x4000;p=end
while r[p-1]==0:p-=1
initoff=(p+15)&~15;assert end-initoff>=20
initaddr=0x4000+initoff%0x4000
patch(initoff,bytes.fromhex('af ea 52 d4 f0 d7 ea d4 d0 c9'),'Reset Curse state every battle')
patch(0x525af,b'\xcd'+initaddr.to_bytes(2,'little')+b'\0\0','Battle init hook','f0d7ead4d0')
# Record actual player Curse execution at selected-move handling. Preserve original xor and hWhoseTurn.
b=Code(0x7d00);b.label('curse');b.emit('fa dc cc fe a5');b.ref('c2','curseret');b.emit('3e 01 ea 52 d4');b.label('curseret');b.emit('af e0 f3 c9');b.label('end');b.raw(far(g.labels['fear'],46));b.emit('cd c3 33 c9')
patch(0x3fd00,b.finish(),'Battle Curse tracking and frightened text')
patch(0x3d723,b'\xcd'+b.labels['curse'].to_bytes(2,'little'),'Track executed Curse','afe0f3')
patch(0x3c6e3,b'\xcd'+b.labels['end'].to_bytes(2,'little'),'Conditional trainer defeat text','cdc333')
patch(0x29fd,far(g.labels['police'],46).ljust(15,b'\0'),'Guard bulletin after ordinary dialogue','fa3ccca72009fa47cca72003cd9938')
patch(0xfbc9,bytes.fromhex('21 50 d4 01 5e 00'),'Clear added saved flags on NEW GAME','21a4d4010a00')
patch(0x134,b'CREEPY MU V1'.ljust(16,b'\0'),'New branch identity')
v=0
for x in r[0x134:0x14d]:v=(v-x-1)&255
r[0x14d]=v;r[0x14e:0x150]=(sum(r[:0x14e])+sum(r[0x150:])&65535).to_bytes(2,'big');assert len(r)==len(base)
(ROOT/'overhaul/Creepy_Black_Mu_v1.gb').write_bytes(r)
(ROOT/'overhaul/manifest.json').write_text(json.dumps(dict(base_sha256=hashlib.sha256(base).hexdigest(),sha256=hashlib.sha256(r).hexdigest(),labels=c.labels,helpers=g.labels,changes=log),indent=2))
(ROOT/'overhaul/dialogue.json').write_text(json.dumps(dialogue,indent=2))
print('Built',len(code6),'bank6 bytes',c.labels)
