# Re-check every hook ever added (v1-v23) against the CURRENT ROM with patchguard:
#   - no jump elsewhere in the ROM lands inside a patched range (except reviewed, allow-listed ones)
#   - stubs don't leave registers changed that the original code after the hook still reads, and don't
#     re-run a replaced "call X" after changing X's inputs.
# Usage (from overhaul/): python check_hooks.py [ROM]   -> exit code 1 on any unreviewed problem.
import json,sys,hashlib
from patchguard import check_hook,jumps_into,fo
LATEST=sys.argv[1] if len(sys.argv)>1 else 'Creepy_Black_Mu_v23.gb'
cur=open(LATEST,'rb').read()
v1=bytearray(open('Creepy_Black_Mu_v1.gb','rb').read())
# v1 had no byte log: original bytes from the asserts in edit/build.py
V1_HOOKS={0x18e5b:'fa4bd7cb67',0xce2a:'21a24e',0xcd99:'21a4d4',0x1ce27:'214bd7cbde',0x525af:'f0d7ead4d0',
          0x3d723:'afe0f3',0x3c6e3:'cdc333',0x29fd:'fa3ccca72009fa47cca72003cd9938'}
v0=bytearray(v1)
for o,h in V1_HOOKS.items():b=bytes.fromhex(h);v0[o:o+len(b)]=b
roms={0:bytes(v0)}
for v in range(1,99):
    try:roms[v]=open('Creepy_Black_Mu_v%d.gb'%v,'rb').read()
    except FileNotFoundError:break
hooks={}    # site -> (first version, length, original-code ROM)
for o,h in V1_HOOKS.items():hooks[o]=(1,len(bytes.fromhex(h)),roms[0])
for v in range(2,max(roms)+1):
    m=json.load(open('manifest_v%d.json'%v))
    for c in m['changes']:
        o=int(c['offset'],16);a=bytes.fromhex(c['after']);b=bytes.fromhex(c['before'])
        if o in hooks or not a or a[0] not in (0xcd,0xc3) or not any(b) or len(a)>16:continue
        if b[0] not in (0xcd,0xc3,0xfa,0x21,0x3e,0xaf,0xf0,0x06,0x11,0x01,0x7e,0x2a,0xcb,0xea,0xe0,0xa7):continue  # data patches
        hooks[o]=(v,len(a),roms[v-1])
# Reviewed exceptions: (site, 'jump'|'regs') -> reason. Every entry was checked by disassembly; add new ones only
# with the same care and a reason.
REVIEWED={
 (0x15c6,'jump'):'hits are operand bytes (bank C sprite data at 0x315CF, "ld [$cc3c],a" operand at 0x74E11)',
 (fo(0xe,0x58c6),'jump'):'"cp $28" operand at E:589D',
 (fo(3,0x79da),'regs'):'heal-skip stub advances hl/de to the next Pokemon on purpose (it is the loop iterator)',
 (fo(0xf,0x5804),'regs'):'player animation hook changes a (= animation id) on purpose',
 (fo(0xf,0x689f),'regs'):'enemy animation hook changes a (= animation id) on purpose',
 (0x29fd,'jump'):'v13 layout: 0x2A03 (AfterDisplayingTextID) is the first byte of the far call again; 0x2A06/0x2A07 hits are operand/data bytes',
 (0x1395e,'jump'):'v3 retargeted the two encounter jr\'s to 0x7961 on purpose; 0x13993 is the operand of "srl b"',
 (0xff8e,'jump'):'hits come from text data in bank 3',
 (fo(0x17,0x50b0),'jump'):'v14: 17:50FD is Saffron Gym trainer-header data (30 b3 d7 = sight 3, event byte D7B3), not a jr',
 (0x62d,'jump'):'hits are operand/data bytes (0x335e, 0x8ac9, 0x20d71, 0x7cb3e)',
 (0xc4,'jump'):'0x4c42 is an operand byte',
 (0x18e5b,'jump'):'v1 Pallet stub jumps back to 0x4E60 = the untouched instruction after the patch',
}
RESULT_FLAG_HOOKS={fo(0xf,0x5033):'f',fo(0xf,0x5920):'f',fo(0x16,0x4dd8):'b f',fo(3,0x61b9):'a f',fo(3,0x79da):'a f',
                   fo(0xf,0x57d3):'',fo(0xf,0x6865):'',fo(4,0x795e):'a f',fo(0xf,0x4ae4):'a f',fo(0xf,0x58e2):'a f',
                   fo(0xf,0x6218):'h l',fo(0xf,0x62d6):'h l',fo(0xe,0x5c91):'a',0x15c6:'a',fo(0xf,0x4233):'',
                   fo(0xf,0x7d08):'',fo(0xf,0x689f):'',fo(0xf,0x5804):'',fo(0xe,0x58c6):'h l b c',fo(0xf,0x6403):'h l b c',
                   fo(0xf,0x6bc6):'h l b c',fo(3,0x77af):'h l b c',fo(3,0x69d7):'h l b c',fo(3,0x79fa):'h l b c',fo(0xe,0x70a6):'h l b c',
                   0xcd99:'h l',0x3d723:'a',fo(0xf,0x572d):'a',
                   fo(0xf,0x5000):'a f'}   # v23 battle menu: a = the selection again, flags set by the stub's own path
problems=0;report=[]
for site in sorted(hooks):
    v,length,before=hooks[site]
    if cur[site] not in (0xcd,0xc3) and site!=0x29fd:continue   # hook removed later
    prov=tuple(RESULT_FLAG_HOOKS.get(site,'').split())
    if site==0x29fd:
        # v13 layout: fa 3c cc / a7 / 20 09 / [0x2A03] 21 .. / 06 2e / cd 18 36 / 00. Real entries are 0x2A03;
        # 0x2A06/0x2A07 hits come from operand/data bytes (checked by disassembly).
        hits=jumps_into(cur,site,length);starts={0x29fd,0x2a00,0x2a01,0x2a03,0x2a06,0x2a08,0x2a0b}
        bad=[(s,t) for s,t in hits if t not in starts and s!=0x740]     # 0x740 = operand bytes of "jp $07c4" at 0x73F
        ok=cur[0x2a03]==0x21 and not bad
        report.append((site,v,'OK' if ok else 'PROBLEM',['%d jump(s) land on instruction starts of the v13 layout'%len(hits)] if ok else ['bad: %s'%bad]));continue
    pr=check_hook(before,cur,site,length,provides=prov)
    jumps=[p for p in pr if p.startswith('jump')];regs=[p for p in pr if not p.startswith('jump')]
    status='OK'
    if jumps and (site,'jump') in REVIEWED:jumps=['%d jump hit(s) reviewed: %s'%(len(jumps),REVIEWED[(site,'jump')])]
    elif jumps:status='PROBLEM'
    if regs and (site,'regs') in REVIEWED:regs=['reviewed: '+REVIEWED[(site,'regs')]]
    elif regs:status='PROBLEM'
    report.append((site,v,status,jumps+regs))
for site,v,status,pr in report:
    b=site//0x4000;a=site if b==0 else 0x4000+site%0x4000
    print('%-8s v%-2d %02x:%04x  %s'%(status,v,b,a,' | '.join(pr)))
    if status=='PROBLEM':problems+=1
print('%d hooks checked, %d problem(s)'%(len(report),problems))
sys.exit(1 if problems else 0)
