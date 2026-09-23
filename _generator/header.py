import random, math
from common import *
random.seed(7)
W,H=320,150
HZ=100
b=[]
# sky bands with dither
bands=['#1f1540','#2e1a52','#4a2466','#6e2f73','#9a3d74','#c75068','#e8705a','#f7964c','#ffbf5e']
bh=HZ/len(bands)
for i,c in enumerate(bands):
    b.append(f'<rect x="0" y="{i*bh:.0f}" width="{W}" height="{bh+1:.0f}" fill="{c}"/>')
defs=[]
for i in range(len(bands)-1):
    y=round((i+1)*bh)
    defs.append(f'<pattern id="d{i}" width="2" height="2" patternUnits="userSpaceOnUse"><rect width="2" height="2" fill="{bands[i]}"/><rect width="1" height="1" fill="{bands[i+1]}"/><rect x="1" y="1" width="1" height="1" fill="{bands[i+1]}"/></pattern>')
    b.append(f'<rect x="0" y="{y-2}" width="{W}" height="2" fill="url(#d{i})"/>')
# stars
stars=[]
for k in range(40):
    x=random.randint(0,W-1); y=random.randint(0,34)
    stars.append(f'<rect class="tw" style="animation-delay:{random.uniform(0,4):.2f}s" x="{x}" y="{y}" width="1" height="1" fill="#fff4d6"/>')
b+=stars
# sun
SX,SY,R=262,76,16
glow=[(x,y) for x in range(SX-R-6,SX+R+7) for y in range(SY-R-6,HZ) if (x-SX)**2+(y-SY)**2<=(R+5)**2]
sun=[(x,y) for x in range(SX-R,SX+R+1) for y in range(SY-R,HZ) if (x-SX)**2+(y-SY)**2<=R**2]
core=[(x,y) for (x,y) in sun if (x-SX)**2+(y-SY+4)**2<=(R-5)**2]
b.append(f'<path class="glow" d="{rects_path(glow)}" fill="#ffcf6e" opacity=".35"/>')
b.append(f'<path d="{rects_path(sun)}" fill="#ffb347"/>')
b.append(f'<path d="{rects_path(core)}" fill="#ffe7a0"/>')
# sun stripes (retro)
for k,yy in enumerate([88,92,95,97]):
    b.append(f'<rect x="{SX-R}" y="{yy}" width="{2*R+1}" height="{1}" fill="#f7964c"/>')
# clouds
def cloud(x,y,l,c1,c2):
    cells=[(x+i,y) for i in range(l)]+[(x+3+i,y-1) for i in range(l-8)]+[(x+6+i,y-2) for i in range(max(2,l-16))]
    under=[(x+2+i,y+1) for i in range(l-4)]
    return f'<path d="{rects_path(cells)}" fill="{c1}"/><path d="{rects_path(under)}" fill="{c2}"/>'
cl1=cloud(0,50,34,'#f7a36b','#c65b7c')+cloud(60,58,24,'#f4b07a','#b85478')
cl2=cloud(150,40,28,'#e88a78','#9a3d74')+cloud(250,62,20,'#ffc98a','#d06a6a')
b.append(f'<g class="c1"><g>{cl1}</g><g transform="translate({W} 0)">{cl1}</g></g>')
b.append(f'<g class="c2"><g>{cl2}</g><g transform="translate({W} 0)">{cl2}</g></g>')
# mountains (Beydaglari across the bay)
def ridge(x0,x1,base,top,rough,seed):
    random.seed(seed); h=[]; y=base-4
    for x in range(x0,x1):
        peak=top+ (base-top)*(0.5+0.5*math.cos((x-x0)/(x1-x0)*math.pi*2.2))
        y+=random.choice([-1,0,0,1])*rough; y=max(top,min(base,int(0.7*y+0.3*peak)))
        h.append((x,y))
    return h
far=ridge(100,W,HZ,64,2,3)
near=ridge(150,W,HZ,74,2,11)
b.append(f'<path d="{rects_path([(x,y) for x,t in far for y in range(t,HZ)])}" fill="#7a3a78"/>')
b.append(f'<path d="{rects_path([(x,t) for x,t in far])}" fill="#d9707a"/>')
b.append(f'<path d="{rects_path([(x,y) for x,t in near for y in range(t,HZ)])}" fill="#4a2358"/>')
b.append(f'<path d="{rects_path([(x,t) for x,t in near if x<SX])}" fill="#b04e6e"/>')
# sea
sea=['#3a2a5e','#2f3a6e','#27497a','#205a86','#1d6690']
for i,c in enumerate(sea):
    b.append(f'<rect x="0" y="{HZ+i*10}" width="{W}" height="10" fill="{c}"/>')
# reflection strips under sun
random.seed(5)
for k in range(16):
    y=HZ+2+k*3; w=max(4,int(30-k*1.2+random.randint(-3,3))); x=SX-w//2+random.randint(-3,3)
    col='#ffe7a0' if k<4 else ('#ffbf5e' if k<9 else '#f7964c')
    b.append(f'<rect class="sh" style="animation-delay:{k*0.23:.2f}s" x="{x}" y="{y}" width="{w}" height="1" fill="{col}"/>')
# wave glints
waves=[]
for k in range(46):
    x=random.randint(0,W); y=random.randint(HZ+4,H-2); l=random.randint(3,7)
    waves.append(f'<rect class="wv" style="animation-delay:{random.uniform(0,3):.2f}s" x="{x}" y="{y}" width="{l}" height="1" fill="#7fb6d6"/>')
b+=waves
# boat (gulet)
boat=[
"......W.......",
".....WW.......",
"....WWW..W....",
"...WWWW..WW...",
"..WWWWW..WWW..",
".WWWWWW..WWWW.",
"......M....M..",
"BBBBBBBBBBBBBBB",
".bBBBBBBBBBBBb.",
"..bbbbbbbbbbb..",
]
bs=sprite(boat,0,0,{'W':'#fff1d6','M':'#6b3a2a','B':'#8a4a32','b':'#5a2e22'})
b.append(f'<g class="boat"><g class="bob">{bs}<rect x="1" y="10" width="13" height="1" fill="#0f2f4f" opacity=".6"/></g></g>')
# gulls
g1=["W...W",".W.W.","..W.."]; g2=[".....","WWWWW","..W.."]
def gull(x,y,d):
    return (f'<g class="gull" style="animation-delay:{d}s" transform="translate({x} {y})"><g class="f1">{sprite(g1,0,0,{"W":"#2a1640"})}</g>'
            f'<g class="f2">{sprite(g2,0,0,{"W":"#2a1640"})}</g></g>')
b.append(f'<g class="gulls">{gull(60,70,0)}{gull(72,64,.2)}{gull(52,62,.4)}</g>')
# cliff with Kaleici houses + Yivli Minare
cliff=[]
random.seed(2)
edge=[]
for x in range(0,96):
    top=88 + int(max(0,(x-70))*0.5) + random.choice([0,0,1])
    edge.append((x,top))
    for y in range(top,H): cliff.append((x,y))
b.append(f'<path d="{rects_path(cliff)}" fill="#3b1f3a"/>')
b.append(f'<path d="{rects_path([(x,t) for x,t in edge])}" fill="#8a4a5a"/>')
# cliff texture
tex=[(random.randint(0,90),random.randint(92,H-1)) for _ in range(120)]
b.append(f'<path d="{rects_path(tex)}" fill="#2a1530"/>')
# houses
houses=[(4,10,8),(15,12,10),(28,9,7),(50,11,9),(62,10,11),(74,9,7)]
hb=[]; wins=[]
for i,(x,w,h) in enumerate(houses):
    top=88-h
    hb.append(f'<rect x="{x}" y="{top}" width="{w}" height="{h}" fill="#e6b889"/>')
    hb.append(f'<rect x="{x}" y="{top}" width="{w}" height="{h}" fill="#5a2a4a" opacity=".45"/>')
    hb.append(f'<rect x="{x-1}" y="{top-2}" width="{w+2}" height="2" fill="#b0463a"/>')
    hb.append(f'<rect x="{x}" y="{top-3}" width="{w}" height="1" fill="#d0654a"/>')
    for wx in range(x+2,x+w-1,3):
        for wy in range(top+2,88-2,4):
            wins.append(f'<rect class="win" style="animation-delay:{random.uniform(0,6):.2f}s" x="{wx}" y="{wy}" width="1" height="2" fill="#ffd36b"/>')
b+=hb+wins
# minaret
mx=40
mn=[f'<rect x="{mx}" y="60" width="6" height="28" fill="#b5553f"/>',
    f'<rect x="{mx+1}" y="60" width="1" height="28" fill="#d9775a"/>',f'<rect x="{mx+3}" y="60" width="1" height="28" fill="#d9775a"/>',
    f'<rect x="{mx+5}" y="60" width="1" height="28" fill="#7a3030"/>',
    f'<rect x="{mx-1}" y="66" width="8" height="2" fill="#e6b889"/>',
    f'<rect x="{mx}" y="56" width="6" height="4" fill="#e6b889"/>',
    f'<rect x="{mx+1}" y="52" width="4" height="4" fill="#8a9aa8"/>',f'<rect x="{mx+2}" y="48" width="2" height="4" fill="#8a9aa8"/>',
    f'<rect x="{mx+2}" y="46" width="1" height="2" fill="#ffd36b"/>',
    f'<rect class="win" x="{mx+2}" y="57" width="2" height="2" fill="#ffd36b"/>']
b+=mn
b.append(f'<rect x="{mx-2}" y="86" width="12" height="2" fill="#6a3040"/>')
# palms
def palm(x,y):
    s=["..GG.GG..",".G..G..G.","G..GGG..G","...GTG...","....T....","....T....","....T....","....T....","....T....","...TTT..."]
    return sprite(s,x,y,{'G':'#2e6a4a','T':'#5a3a2a'})
b.append(f'<g class="palm">{palm(84,78)}</g>')
# title
b.append(text('SARP SOLAZAN',160,12,'#fff4d6',2,anchor='middle',shadow='#3a1d4a'))
b.append(text('WEB3 PRODUCT BUILDER',160,36,'#ffd36b',1,anchor='middle',shadow='#3a1d4a'))
b.append(text('ANTALYA, TR',160,48,'#f4b8a0',1,anchor='middle',shadow='#3a1d4a'))
b.append(text('PRESS START',262,136,'#fff4d6',1,cls='blink',anchor='middle',shadow='#0f2f4f'))
b.append(f'<g class="blink"><path d="M218 136h1v7h-1zM219 137h1v5h-1zM220 138h1v3h-1zM221 139h1v1h-1z" fill="#ffd36b"/></g>')
# frame
b.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="none" stroke="#1a0f2e" stroke-width="2"/>')
style='''
.tw{animation:tw 3s steps(2) infinite}@keyframes tw{0%,100%{opacity:.9}50%{opacity:.15}}
.glow{animation:gl 4s steps(4) infinite}@keyframes gl{0%,100%{opacity:.25}50%{opacity:.5}}
.sh{animation:sh 2.4s steps(3) infinite}@keyframes sh{0%,100%{opacity:1}50%{opacity:.25}}
.wv{animation:wv 3s steps(3) infinite}@keyframes wv{0%,100%{opacity:0;transform:translateX(0)}50%{opacity:.8;transform:translateX(3px)}}
.c1{animation:mv 90s linear infinite}.c2{animation:mv 60s linear infinite}@keyframes mv{from{transform:translateX(0)}to{transform:translateX(-320px)}}
.boat{animation:boat 48s linear infinite}@keyframes boat{from{transform:translate(330px,110px)}to{transform:translate(40px,110px)}}
.bob{animation:bob 1.6s steps(2) infinite}@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(1px)}}
.gulls{animation:gs 30s linear infinite}@keyframes gs{from{transform:translateX(-80px)}to{transform:translateX(300px)}}
.f1{animation:fa .6s steps(1) infinite}.f2{animation:fb .6s steps(1) infinite}
@keyframes fa{0%{opacity:1}50%{opacity:0}}@keyframes fb{0%{opacity:0}50%{opacity:1}}
.win{animation:win 7s steps(1) infinite}@keyframes win{0%{opacity:.25}30%{opacity:1}85%{opacity:1}92%{opacity:.25}}
.blink{animation:bl 1.2s steps(1) infinite}@keyframes bl{0%{opacity:1}50%{opacity:0}}
'''
body=f'<defs>{"".join(defs)}</defs>'+''.join(b)
open('assets/header.svg','w').write(svg(W,H,body,style,'Sarp Solazan, Web3 product builder from Antalya'))
