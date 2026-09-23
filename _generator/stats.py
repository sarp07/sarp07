from card import *
W,H=320,156
b=[f'<rect width="{W}" height="{H}" fill="{C["bg"]}"/>']
# bg dots
import random; random.seed(4)
b.append(f'<path d="{rects_path([(random.randint(0,W-1),random.randint(0,H-1)) for _ in range(90)])}" fill="#3a2a66"/>')
b.append(window(6,8,76,98,'HERO'))
b.append(window(90,8,224,98,'STATUS'))
b.append(window(6,114,308,36))
# avatar 24x28 sprite at scale 2 -> 48x56 centered in hero window
av=[
"........HHHHHHH.........",
"......HHHHHHHHHHH.......",
".....HHHHHHHHHHHHH......",
"....HHHhHHHHHhHHHHH.....",
"....HHSSSSSSSSSSHHH.....",
"....HSSSSSSSSSSSSHH.....",
"....HSSEESSSSEESSH......",
"....SSSEESSSSEESSS......",
"....SSSSSSSSSSSSSS......",
".....SSSSSnnSSSSS.......",
".....BBSSSSSSSSBB.......",
".....BBBBSmmSBBBB.......",
"......BBBBBBBBBB........",
".......BBBBBBBB.........",
"....OOOOSSSSSSOOOO......",
"..OOOOOOOSSSSOOOOOOO....",
".OOOOOOOOOSSOOOOOOOOO...",
".OOOOOoOOOOOOOOOoOOOO...",
".OOOOOoOOOOOOOOOoOOOO...",
".OOOOOoOOOOOOOOOoOOOO...",
".OOOOLLLLLLLLLLLLLOOO...",
".OOOOLccccccccccLOOOO...",
".SSSSLcgcgggcgcgLSSSS...",
".SSSSLccccccccccLSSSS...",
".OOOOLLLLLLLLLLLLOOOO...",
"LLLLLLLLLLLLLLLLLLLLLL..",
"..........................",
]
pal={'H':'#2a1a14','h':'#4a3024','S':'#e8b08a','E':'#1b1236','n':'#c98a6a','B':'#2a1a14','m':'#b8604a','O':'#f7964c','o':'#c46a3a','L':'#8a9aa8','c':'#1b1236','g':'#7cf2a0'}
avs=sprite(av,0,0,pal)
eyes_closed=f'<g class="eyes"><rect x="7" y="6" width="2" height="2" fill="#e8b08a"/><rect x="13" y="6" width="2" height="2" fill="#e8b08a"/><rect x="7" y="7" width="2" height="1" fill="#1b1236"/><rect x="13" y="7" width="2" height="1" fill="#1b1236"/></g>'
b.append(f'<g transform="translate(20 28) scale(2)"><g class="idle">{avs}{eyes_closed}<g class="code">'
         f'<rect x="7" y="22" width="1" height="1" fill="#ffd36b"/><rect x="11" y="22" width="1" height="1" fill="#e8705a"/></g></g></g>')
b.append(f'<rect x="12" y="90" width="64" height="12" fill="{C["sh"]}"/>')
b.append(text('LV 99',44,92,C['gold'],anchor='middle'))
# status
rows=[('NAME','SARP SOLAZAN'),('CLASS','WEB3 BUILDER'),('BASE','ANTALYA, TR'),('PARTY','OWN CREW')]
for i,(k,v) in enumerate(rows):
    y=17+i*11
    b.append(text(k,100,y,C['dim'])); b.append(text(v,156,y,C['txt']))
bars=[('FULL STACK',0.95,C['gold']),('WEB3/DEFI',0.92,C['org']),('DEVOPS',0.85,C['pink']),('PRODUCT',0.9,'#7cf2a0')]
for i,(k,v,c) in enumerate(bars):
    y=62+i*10
    # label small: use text at scale 1 but narrower? keep 8px, shorter labels
    lab=k
    b.append(f'<g>{text(lab,100,y-1,C["dim"])}</g>')
    bx,bw=196,108
    b.append(f'<rect x="{bx}" y="{y}" width="{bw}" height="5" fill="{C["sh"]}"/>')
    fw=int((bw-2)*v)
    b.append(f'<rect class="bar" style="animation-delay:{i*0.25}s" x="{bx+1}" y="{y+1}" width="{fw}" height="3" fill="{c}"/>')
    b.append(f'<rect class="bar" style="animation-delay:{i*0.25}s" x="{bx+1}" y="{y+1}" width="{fw}" height="1" fill="#fff4d6" opacity=".5"/>')
# dialogue typewriter
l1='SARP: I TAKE WEB3 PRODUCTS FROM ZERO'
l2='TO LAUNCH, A TO Z, WITH MY OWN CREW.'
b.append(text(l1,14,122,C['txt'])); b.append(text(l2,14,134,C['txt']))
n1,n2=len(l1),len(l2)
b.append(f'<rect class="t1" x="13" y="121" width="{width(l1)+2}" height="10" fill="{C["win2"]}"/>')
b.append(f'<rect class="t2" x="13" y="133" width="{width(l2)+2}" height="10" fill="{C["win2"]}"/>')
b.append(f'<path class="cur" d="M300 138h7v1h-1v1h-1v1h-1v1h-1v-1h-1v-1h-1v-1h-1z" fill="{C["gold"]}"/>')
style=f'''
.idle{{animation:idle 1.4s steps(1) infinite}}@keyframes idle{{0%{{transform:translateY(0)}}50%{{transform:translateY(1px)}}}}
.eyes{{opacity:0;animation:eye 4s steps(1) infinite}}@keyframes eye{{0%,92%{{opacity:0}}94%{{opacity:1}}98%{{opacity:0}}}}
.code rect{{animation:bl .5s steps(1) infinite}}.code rect+rect{{animation-delay:.25s}}
.bar{{transform-box:fill-box;transform-origin:left;animation:fill 10s steps(24) infinite}}
@keyframes fill{{0%{{transform:scaleX(0)}}15%,100%{{transform:scaleX(1)}}}}
.t1,.t2{{transform-box:fill-box;transform-origin:right}}.t1{{animation:ty1 10s steps({n1},end) infinite}}.t2{{animation:ty2 10s steps({n2},end) infinite}}
@keyframes ty1{{0%{{transform:scaleX(1)}}30%,100%{{transform:scaleX(0)}}}}
@keyframes ty2{{0%,30%{{transform:scaleX(1)}}60%,100%{{transform:scaleX(0)}}}}
.cur{{animation:bl 1s steps(1) infinite}}@keyframes bl{{0%{{opacity:1}}50%{{opacity:0}}}}
'''
open('assets/stats.svg','w').write(svg(W,H,''.join(b),style,'Character card: Sarp Solazan, Web3 builder'))
