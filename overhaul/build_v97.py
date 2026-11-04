# Creepy Black Mu v97 (on v96): MR. MU's first question says "while fighting for its TRAINER" instead of "while obeying its TRAINER".
#   The speech at 31:6200 (v65) is rewritten in place; it grows by a few bytes into the free space before 31:6400 (pal66).
from patchlib import *
from patchguard import fo
V96_SHA='3e6ba0459eb7e07b829d3a73547f730e64249cfc5020ba8c6379ed745cc491ff'
rom=Rom('Creepy_Black_Mu_v96.gb',V96_SHA)
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
old=speech([["If a #MON","kills a person","while obeying its","TRAINER..."],["Who is","responsible?"]])
new=speech([["If a #MON","kills a person","while fighting","for its","TRAINER..."],["Who is","responsible?"]])
o=fo(0x31,0x6200)
assert R[o:o+len(old)]==old,'v65 speech not found'
assert len(new)>=len(old) and not any(R[o+len(old):o+len(new)]) and 0x6200+len(new)<=0x6400
rom.data(o,new,"MR. MU's first question: 'while fighting for its TRAINER'",R[o:o+len(new)].hex())
rom.finish('Creepy_Black_Mu_v97.gb','manifest_v97.json','CREEPY MU V97')
