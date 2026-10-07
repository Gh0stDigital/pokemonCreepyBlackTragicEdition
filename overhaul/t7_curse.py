from harness import *
load('after_rival')
# Ghost to lead (swap party slot data/species), redirect lab exit warp to Viridian Forest
a=list(m[0xd16b:0xd197]);b=list(m[0xd197:0xd1c3]);m[0xd16b:0xd197]=b;m[0xd197:0xd1c3]=a
m[0xd164],m[0xd165]=m[0xd165],m[0xd164]
na=list(m[0xd2b5:0xd2c0]);nb=list(m[0xd2c0:0xd2cb]);m[0xd2b5:0xd2c0]=nb;m[0xd2c0:0xd2cb]=na
oa=list(m[0xd273:0xd27e]);ob=list(m[0xd27e:0xd289]);m[0xd273:0xd27e]=ob;m[0xd27e:0xd289]=oa
m[0xd3b1]=2;m[0xd3b2]=0x33;m[0xd3b5]=2;m[0xd3b6]=0x33
p.button('down',150);p.tick(150);print('map',pos())
save('forest_entry')
m[0xc224]=m[0xd361]+3;m[0xc225]=m[0xd362]+4   # trainer sprite 2 one tile above player
m[0xd455]=20;m[0xd456]=0
p.tick(60);press('up',20);press('a',300);save('forest_engaged')
print('in battle',m[0xd057],'trainer class',hex(m[0xd031]),'lead species',hex(m[0xd014]))
seen=[];black=0;st=[]
for i in range(160):
    b=box()
    if b and (not seen or seen[-1]!=b):seen.append(b)
    if i>6 and m[0xd057]==0:break
    if 'change' in b or 'Bring out' in b:p.button('b',8)
    else:p.button('a',8)
    for _ in range(200):
        p.tick(1)
        if m[0xff47]==0xff:black+=1
    st.append((m[0xd452],m[0xd453],m[0xd455]))
for s in seen:print('  TEXT:',s.replace('│','').replace('─','').replace('┌','').replace('┐','').replace('└','').replace('┘',''))
print('curse_used',m[0xd452],'ghost_use_counter',m[0xd45c],'killed',m[0xd453],'hunger',m[0xd455],'black frames',black,'gravestones',list(m[0xd4a4:0xd4ae]))
save('after_curse');shot('fear_text_end')
