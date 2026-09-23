from common import *
import random, math
W,H=320,84
b=[]
sky=['#120c2a','#1a1238','#241848','#2e1d55']
for i,c in enumerate(sky): b.append(f'<rect y="{i*14}" width="{W}" height="15" fill="{c}"/>')
random.seed(21)
for k in range(50):
    b.append(f'<rect class="tw" style="animation-delay:{random.uniform(0,3):.2f}s" x="{random.randint(0,W)}" y="{random.randint(0,50)}" width="1" height="1" fill="#fff4d6"/>')
# moon
mc=[(x,y) for x in range(292,312) for y in range(26,46) if (x-302)**2+(y-36)**2<=81]
mcut=[(x,y) for x,y in mc if (x-306)**2+(y-33)**2<=49]
b.append(f'<path d="{rects_path(mc)}" fill="#fff1c8"/><path d="{rects_path(mcut)}" fill="#1a1238"/>')
# layers that scroll: build pattern width W, duplicate
def ridge(seed,base,amp,rough):
    random.seed(seed); y=base; out=[]
    for x in range(W):
        y+=random.choice([-1,0,1])*rough
        target=base-amp*(0.5+0.5*math.sin(x/W*2*math.pi*2))
        y=int(0.8*y+0.2*target); out.append((x,y))
    # make seamless: blend end to start
    return out
def layer(seed,base,amp,rough,col,top):
    r=ridge(seed,base,amp,rough)
    for i in range(20):
        x,y=r[W-20+i]; y0=r[0][1]; r[W-20+i]=(x,int(y+(y0-y)*(i+1)/20))
    cells=[(x,y) for x,t in r for y in range(t,70)]
    return f'<path d="{rects_path(cells)}" fill="{col}"/><path d="{rects_path([(x,t) for x,t in r])}" fill="{top}"/>'
far=layer(1,50,14,1,'#3a2360','#5a3a80')
mid=layer(5,60,8,1,'#2a1848','#4a2e6a')
b.append(f'<g class="p1"><g>{far}</g><g transform="translate({W} 0)">{far}</g></g>')
b.append(f'<g class="p2"><g>{mid}</g><g transform="translate({W} 0)">{mid}</g></g>')
# trees + signpost on ground layer
tree=["...G...","..GGG..",".GGGGG.","..GGG..",".GGGGG.","GGGGGGG","...T...","...T..."]
def trees():
    s=''
    for x in [10,46,90,150,205,240,300]:
        s+=sprite(tree,x,62,{'G':'#1f4a3a','T':'#3a2418'})
    sign=["SSSSSSSS","SSSSSSSS","...P....","...P....","...P...."]
    s+=sprite(sign,176,63,{'S':'#b5553f','P':'#5a3a2a'})
    s+='<rect x="177" y="64" width="6" height="1" fill="#ffd36b"/>'
    return s
tr=trees()
b.append(f'<rect y="70" width="{W}" height="14" fill="#2a1a2e"/>')
b.append(f'<rect y="70" width="{W}" height="1" fill="#6a4a5a"/>')
gd=''.join(f'<rect x="{x}" y="{74+(x%3)*3}" width="3" height="1" fill="#3e2a3e"/>' for x in range(0,W,11))
b.append(f'<g class="p3"><g>{tr}{gd}</g><g transform="translate({W} 0)">{tr}{gd}</g></g>')
# walker: backpacker 12x14, two frames
body=["....HHHH....","...HHHHHH...","...HSSSSH...","...SSESES...","....SSSS....","..PPOOOO....","..PPOOOOS...","..PPOOOOS...","..PPOOOO....","....BBBB....","....BBBB...."]
leg1=["....B..B....","...B....B...","..KK....KK.."]
leg2=["....BB......","....BB......","....KKK....."]
pal={'H':'#2a1a14','S':'#e8b08a','E':'#1b1236','O':'#f7964c','P':'#4a6a8a','B':'#3a3a6a','K':'#1b1236'}
wx,wy=120,56
w=(f'<g class="bob">{sprite(body,wx,wy,pal)}</g>'
   f'<g class="f1">{sprite(leg1,wx,wy+11,pal)}</g><g class="f2">{sprite(leg2,wx,wy+11,pal)}</g>')
# stick
w+=f'<rect x="{wx+9}" y="{wy+5}" width="1" height="10" fill="#8a5a3a"/>'
b.append(w)
from pixfont import text as T
b.append(T('THANKS FOR STOPPING BY, TRAVELER',160,14,'#fff4d6',anchor='middle',shadow='#0e0820'))
b.append(T('GAME SAVED',160,28,'#ffd36b',cls='blink',anchor='middle',shadow='#0e0820'))
b.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="none" stroke="#1a0f2e" stroke-width="2"/>')
style='''
.tw{animation:tw 2.5s steps(2) infinite}@keyframes tw{0%,100%{opacity:.9}50%{opacity:.1}}
.p1{animation:mv 80s linear infinite}.p2{animation:mv 40s linear infinite}.p3{animation:mv 16s linear infinite}
@keyframes mv{from{transform:translateX(0)}to{transform:translateX(-320px)}}
.f1{animation:fa .5s steps(1) infinite}.f2{animation:fb .5s steps(1) infinite}
@keyframes fa{0%{opacity:1}50%{opacity:0}}@keyframes fb{0%{opacity:0}50%{opacity:1}}
.bob{animation:bob .5s steps(1) infinite}@keyframes bob{0%{transform:translateY(0)}50%{transform:translateY(1px)}}
.blink{animation:bl 1.2s steps(1) infinite}@keyframes bl{0%{opacity:1}50%{opacity:0}}
'''
open('assets/footer.svg','w').write(svg(W,H,''.join(b),style,'Thanks for stopping by'))
