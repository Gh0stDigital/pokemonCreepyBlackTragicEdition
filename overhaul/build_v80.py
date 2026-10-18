# Creepy Black Mu v80: as BLACK, ordinary (non-gym) trainers who are alive talk to you scared: pleading, refusing to fight for their lives/souls,
#   offering their POKeMON. 24 lines before the battle, 16 after it, picked by kill index. Gym trainers, dead trainers, scripted trainers: unchanged.
#   New dispatcher rdisp80 (home stub 0:00CE) checks BLACK (D46C), not a gym map, header trainer (kill index != 0), not dead; else jumps to v69's rdisp69.
import json
from patchlib import *
from patchguard import fo
from sm83asm import asm

V79_SHA='71445e6b2dba1c90662197a7ce5b6143879aeadd3766d76c0ca9a89816ac0717'
rom=Rom('Creepy_Black_Mu_v79.gb',V79_SHA)
R=bytes(rom.r)
B31=0x31;CODE=0x4c00;TXT=0x5000
assert not any(R[fo(B31,CODE):fo(B31,0x5800)])
L69={k:int(v,16) for k,v in json.load(open('manifest_v69.json'))['labels']['bank31'].items()}
def T(paras):return bytes(txt(paras,0x58,17))
PRE=[
 [["No! Please! I","have a family!","Take my POKeMON!"]],
 [["Don't hurt me!","I'll give you","all my POKeMON."]],
 [["Not my soul!","Please, anything","but my soul!"]],
 [["I don't want to","fight you. I","won't die here."]],
 [["Here, take my","best POKeMON.","Just let me live."]],
 [["I can feel it","watching me...","Stay back!"]],
 [["Please... my","POKeMON are all","I have. Spare us."]],
 [["I'll do anything!","Just don't use","that thing on me!"]],
 [["You're not human","anymore, are you?","Please, no..."]],
 [["I surrender!","Take them! Take","all of them!"]],
 [["My POKeMON are","shaking. They","know your name."]],
 [["Don't look at me","with those eyes!","I'll fight but..."]],
 [["I never did","anything to you!","Have mercy!"]],
 [["Take my POKeMON","and go. I beg","you. Just go."]],
 [["Everyone says","you eat souls.","Is it true?!"]],
 [["I can't breathe","near you. Please,","let me go."]],
 [["Why me? Why now?","I only wanted a","quiet day..."]],
 [["Fine! Fight me!","But don't take","my soul. Please."]],
 [["Mother, forgive","me... I can't","run away..."]],
 [["Take the POKeMON.","Take my money.","Spare my life!"]],
 [["The air is cold.","It's you... isn't","it?"]],
 [["I won't resist.","Do what you want","with my POKeMON."]],
 [["Please! I'm too","young to be","consumed!"]],
 [["I'll fight, if","you want. Just","leave my soul."]]]
POST=[
 [["Keep them... keep","my POKeMON. Just","stay away."]],
 [["I'm alive...","thank you, thank","you..."]],
 [["Don't come near","me again. Please."]],
 [["Take whatever you","want. I'll never","tell a soul."]],
 [["I can't stop","shaking. Go away."]],
 [["It let me live.","Why did it let me","live?"]],
 [["Just go. I beg","you. Just go."]],
 [["Don't look back","at me. Don't."]],
 [["I'll pray for","you. Or for me.","Just go."]],
 [["Get away! The","POKeMON are all","yours, just GO!"]],
 [["I saw nothing.","I heard nothing.","Please leave."]],
 [["My soul is still","mine... isn't it?","Leave me."]],
 [["Monster... no.","Sorry. Sorry!","Please go."]],
 [["I'll give you","anything, really","to be left alone."]],
 [["Is it over? Is it","really over? Go."]],
 [["Whatever you are,","please go away."]]]
tx=bytearray();TP=[];TQ=[]
for l in PRE:TP.append(TXT+len(tx));tx+=T(l)
for l in POST:TQ.append(TXT+len(tx));tx+=T(l)
assert TXT+len(tx)<0x5800
rom.put(fo(B31,TXT),bytes(tx),'Bank 31: v80 scared trainers\' lines (BLACK)')
tp=''.join(f'    dw {a:#x}\n' for a in TP);tq=''.join(f'    dw {a:#x}\n' for a in TQ)
SRC=f'''
ptab:
{tp}
qtab:
{tq}
rdisp80:
    ld a,[$d46c]
    and a
    jp z,{L69['rdisp69']:#x}
    ld a,[$d35e]
    call {L69['gymfind']:#x}
    jp c,{L69['rdisp69']:#x}
    ld a,[$d4ae]
    ld h,a
    ld a,[$d4af]
    ld l,a
    or h
    jp z,{L69['rdisp69']:#x}       ; kill index 0: not a header trainer that can die
    call {L69['killtest']:#x}
    jp c,{L69['rdisp69']:#x}
    ld a,d
    and a
    jr nz,.after
    ld a,1                        ; before the battle: note a header trainer is fighting (as rdisp69 does)
    ld [$d844],a
    xor a
    ld [$d845],a
    ld a,[$d4af]
    ld hl,ptab
    ld e,24
    jr .go
.after:
    ld [$d845],a
    ld a,[$d4af]
    ld hl,qtab
    ld e,16
.go:
    ld b,a
.m:
    ld a,b
    cp e
    jr c,.ok
    sub e
    ld b,a
    jr .m
.ok:
    ld a,b
    call {L69['pick']:#x}
    call $3c94
    scf
    ret
'''
code,L=asm(SRC,CODE,dict(L69))
assert CODE+len(code)<0x5000
rom.put(fo(B31,CODE),code,'Bank 31: v80 scared-trainer dispatcher')
assert R[0xd1:0xd4].hex()=='21'+L69['rdisp69'].to_bytes(2,'little').hex()
rom.data(0xd2,L['rdisp80'].to_bytes(2,'little'),'Home stub 0:00CE -> rdisp80 (scared trainers as BLACK)',L69['rdisp69'].to_bytes(2,'little').hex())
rom.finish('Creepy_Black_Mu_v80.gb','manifest_v80.json','CREEPY MU V80',extra=dict(labels=dict(bank31={k:hex(v) for k,v in {**L69,**L}.items()})))
