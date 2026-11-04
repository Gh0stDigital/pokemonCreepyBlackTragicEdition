# Creepy Black Mu v98 (on v97): MR. MU's first question: "If a POKeMON kills someone while fighting for its TRAINER..." ("a person" -> "someone").
from patchlib import *
from patchguard import fo
V97_SHA='bea4bca91c01b8af5f2791982b6ad105667d0cac30d5fc3ec8028aa1f43b6274'
rom=Rom('Creepy_Black_Mu_v97.gb',V97_SHA)
R=bytes(rom.r)
def wrap(s,w=17):
    out=[];cur=''
    for word in s.split():
        if cur and len(cur)+1+len(word)>w:out.append(cur);cur=word
        else:cur=(cur+' '+word) if cur else word
    out.append(cur);return out
SPEECH=["Hello young lad. Sorry to intrude on you so suddenly...",
        "But I couldn't help but notice...",
        "You are about to start a journey as a TRAINER, right?",
        "You certainly have the look about you.",
        "I was wondering if you could humor an old man's question."]
def speech(q):return bytes(txt([wrap(s) for s in SPEECH]+q,0x58,17))
old=speech([["If a #MON","kills a person","while fighting","for its","TRAINER..."],["Who is","responsible?"]])
new=speech([["If a #MON","kills someone","while fighting","for its","TRAINER..."],["Who is","responsible?"]])
o=fo(0x31,0x6200)
assert R[o:o+len(old)]==old and len(new)<=len(old)
pad=bytes(len(old)-len(new))
rom.data(o,new+pad,"MR. MU's first question: 'kills someone while fighting for its TRAINER'",R[o:o+len(old)].hex())
rom.finish('Creepy_Black_Mu_v98.gb','manifest_v98.json','CREEPY MU V98')
