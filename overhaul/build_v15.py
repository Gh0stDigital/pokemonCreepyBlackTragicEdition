# Creepy Black Mu v15: BLUE at Nugget Bridge (Cerulean) reacts to the killer, BILL tells the old soul-tribe story.
# Logged patches on top of verified Mu v14 (patchlib).
from patchlib import *
from patchguard import fo

V14_SHA='acd7ac590d4893b0edd0f0a01c5c1227fabd0c8166f1f8f3a14b5241322eeb46'
rom=Rom('Creepy_Black_Mu_v14.gb',V14_SHA)
r=rom.r
PRINTTEXT,TEXTEND=0x3c94,0x2504
GHOST_ROUTE,MURDER,TEMP,MODE=0xd451,0xd453,0xd457,0xd463
EV_CERULEAN_POST=(0xd75a,0)      # Cerulean text 1 shows the after-battle text once this is set (checked in the ROM)
EV_GOT_TICKET=(0xd7f2,4)         # BILL gave the S.S. TICKET
labels={}

T={
 # 1. Nugget Bridge, GHOST route, at least one murder, BLUE not in shock mode
 'cer_pre':[["<RIVAL>: Hey!","<PLAYER>!"],["Have you heard?","Some trainer is","going around","killing people","and #MON too!"],
            ["The POLICE can't","catch him."],["If he came for","you, could you","defend yourself?"],
            ["Let me test you!","Show me you're","ready, <PLAYER>!"]],
 # won without GHOST: then his usual BILL text follows
 'cer_strong':[["<RIVAL>: Hmph!","You really have","gotten stronger."],["But don't get","cocky!"],
               ["Watch your back,","and keep an eye","out for that"],["killer... and","whatever else is","out there!"]],
 # GHOST killed his POKeMON here: shock mode starts (v12 rule), no BILL chat
 'cer_shock':[["<RIVAL>: ...","My #MON..."],["They're dead...","That GHOST of","yours killed","them!"],
              ["Stay away from","me, <PLAYER>!"]],
 'cer_shock_killer':[["<RIVAL>: ...","My #MON..."],["They're dead...","That GHOST of","yours killed","them!"],
                     ["Wait... You...","Are YOU the","killer!?"],["Stay away from","me, <PLAYER>!"]],
 # 2. BILL, once, right after the S.S. TICKET
 'bill_lore':[["BILL: Say...","Can I tell you","something odd?"],
              ["Long before the","LEAGUE, KANTO had","an old tribe."],
              ["They believed the","souls of people","and #MON could","be caught and","bent to their","will."],
              ["Their descendants","are said to have","settled in","LAVENDER TOWN."],
              ["I've been testing","their old ideas","with science!"],
              ["My teleporter","turns #MON","into data..."],
              ["So what is a","soul? Maybe just","data, too..."],
              ["I learned a lot","of this from my","mentor, PROF.OAK."]],
}

g=Code(0x2e,0x5400)
# Cerulean text 1. D457 = 1: handled here, skip the original; 0: run the original text.
g.label('cer');g.emit('af ea %s fa %s a7 c8'%(le(TEMP),le(GHOST_ROUTE)))
g.emit('fa %s cb %02x'%(le(EV_CERULEAN_POST[0]),0x47+8*EV_CERULEAN_POST[1]));g.jr('20','post')
g.emit('fa %s a7 c8 fa %s a7 c0'%(le(MURDER),le(MODE)))                      # murder, not in shock mode
g.ref('21','t_cer_pre');g.jr('18','handled')
# after the battle: mode 1 can only be new here (shock mode before Cerulean skips this battle altogether)
g.label('post');g.emit('fa %s fe 01'%le(MODE));g.jr('20','noshock')
g.ref('21','t_cer_shock');g.emit('fa %s a7'%le(MURDER));g.jr('28','handled');g.ref('21','t_cer_shock_killer')
g.label('handled');g.emit('cd %s 3e 01 ea %s c9'%(le(PRINTTEXT),le(TEMP)))
g.label('noshock');g.emit('a7 c0 fa %s a7 c8'%le(MURDER));g.ref('21','t_cer_strong');g.emit('c3 '+le(PRINTTEXT))
for k in ('cer_pre','cer_shock','cer_shock_killer'):g.label('t_'+k);g.raw(txt(T[k],end=0x57))
g.label('t_cer_strong');g.raw(txt(T['cer_strong']))
g.label('t_bill_lore');g.raw(txt(T['bill_lore'],end=0x57))
code2e=g.finish();assert 0x5400+len(code2e)<0x6000
rom.put(fo(0x2e,0x5400),code2e,'Bank 2E: Nugget Bridge BLUE texts + BILL lore')
labels['bank2e']={k:hex(v) for k,v in g.labels.items()}

# Cerulean City (bank 6) text 1 -> wrapper; original text script at 6:5656 (after its 08 byte at 5655)
CER_TP=fo(6,0x5633)
assert r[CER_TP:CER_TP+2]==bytes.fromhex('5556') and r[fo(6,0x5655)]==0x08
c6=Code(6,0x7500)
c6.label('cer');c6.emit('08 '+far(g.labels['cer'],0x2e)+' fa %s a7 ca 56 56 c3 %s'%(le(TEMP),le(TEXTEND)))
code6=c6.finish();rom.put(fo(6,0x7500),code6,'Bank 6: Cerulean BLUE text wrapper')
rom.data(CER_TP,bytes.fromhex(le(c6.labels['cer'])),'Cerulean text 1 (BLUE) -> v15 wrapper','5556')

# Bill's house (bank 7) text 2 -> wrapper: run BILL's original script (it returns through TextScriptEnd),
# then the lore if the S.S. TICKET was handed over in this talk.
BILL_TP=fo(7,0x6844)+2
assert r[BILL_TP:BILL_TP+2]==bytes.fromhex('8468') and r[fo(7,0x6884)]==0x08 and r[fo(7,0x68c7):fo(7,0x68ca)]==bytes.fromhex('c30425')
c7=Code(7,0x7840)
c7.label('bill');c7.emit('08 fa %s f5 cd 85 68 f1 cb %02x'%(le(EV_GOT_TICKET[0]),0x47+8*EV_GOT_TICKET[1]));c7.jr('20','end')
c7.emit('fa %s cb %02x'%(le(EV_GOT_TICKET[0]),0x47+8*EV_GOT_TICKET[1]));c7.jr('28','end')
c7.ref('21','lore');c7.emit('cd '+le(PRINTTEXT))
c7.label('end');c7.emit('c3 '+le(TEXTEND))
c7.label('lore');c7.emit('17 %s 2e 50'%le(g.labels['t_bill_lore']))
code7=c7.finish();rom.put(fo(7,0x7840),code7,'Bank 7: BILL text wrapper (lore after the S.S. TICKET)')
rom.data(BILL_TP,bytes.fromhex(le(c7.labels['bill'])),"Bill's house text 2 (BILL) -> v15 wrapper",'8468')
labels['bank6']={k:hex(v) for k,v in c6.labels.items()};labels['bank7']={k:hex(v) for k,v in c7.labels.items()}

# 3. v12 bug: shock mode meant to skip the Cerulean BLUE battle but set D75B bit 7, which in this ROM is
#    "beat the Cerulean Rocket thief" (his script at 6:54C8 checks it). BLUE's Cerulean flag is D75A bit 0
#    (his trigger at 6:54F7 and text 1 check it). Shock mode now sets D75A bit 0 and leaves the thief alone.
rom.code(fo(0x2e,0x4b6e),bytes.fromhex('21 5a d7 cb c6'),'Shock mode: skip the Cerulean BLUE battle (D75A.0), not the Rocket thief (D75B.7)','21 5b d7 cb fe')

rom.finish('Creepy_Black_Mu_v15.gb','manifest_v15.json','CREEPY MU V15',extra=dict(labels=labels))
