from card import *
import random
items=[('TS','TYPESCRIPT','LANGUAGE'),('RUST','RUST + AXUM','BACKEND'),('SOL','SOLIDITY','SMART CONTRACTS'),
('REACT','REACT','FRONTEND'),('NEXT','NEXT.JS','FULL STACK'),('RN','REACT NATIVE','MOBILE'),
('NODE','NODE.JS','BACKEND'),('VIEM','VIEM + WAGMI','WEB3 CLIENT'),('TW','TAILWIND + SHADCN','FRONTEND'),
('PG','POSTGRESQL','DATABASE'),('MONGO','MONGODB','DATABASE'),('DOCKR','DOCKER','DEVOPS'),
('AWS','AWS LIGHTSAIL','CLOUD'),('CF','CLOUDFLARE','EDGE + DNS'),('DKPLY','DOKPLOY','DEPLOYS'),
('EVM','EVM CHAINS','L1 + L2'),('SOLNA','SOLANA','CHAIN'),('TON','TON + TG MINI APPS','CHAIN')]
rar={'LANGUAGE':C['gold'],'BACKEND':C['org'],'SMART CONTRACTS':'#7cf2a0','FRONTEND':'#7fd4ff','FULL STACK':'#7fd4ff','MOBILE':'#7fd4ff',
'WEB3 CLIENT':'#7cf2a0','DATABASE':'#c9a0ff','DEVOPS':C['pink'],'CLOUD':C['pink'],'EDGE + DNS':C['pink'],'DEPLOYS':C['pink'],'L1 + L2':'#7cf2a0','CHAIN':'#7cf2a0'}
W=320; cols=6; sw,sh_,gap=46,24,4
gx=12; gy=14
rows=(len(items)+cols-1)//cols
gh=rows*(sh_+gap)-gap
H=gy+gh+10+34+8
b=[f'<rect width="{W}" height="{H}" fill="{C["bg"]}"/>']
random.seed(12)
b.append(f'<path d="{rects_path([(random.randint(0,W-1),random.randint(0,H-1)) for _ in range(90)])}" fill="#3a2a66"/>')
b.append(window(6,gy-6,308,gh+12,'INVENTORY'))
pos=[]
for i,(code,full,cat) in enumerate(items):
    r,c=divmod(i,cols); x=gx+c*(sw+gap); y=gy+r*(sh_+gap)
    pos.append((x,y)); col=rar[cat]
    b.append(f'<rect x="{x}" y="{y}" width="{sw}" height="{sh_}" fill="{C["sh"]}"/>')
    b.append(f'<rect x="{x+1}" y="{y+1}" width="{sw-2}" height="{sh_-2}" fill="#2f2260"/>')
    b.append(f'<rect x="{x+1}" y="{y+1}" width="{sw-2}" height="2" fill="{col}"/>')
    b.append(f'<rect x="{x+sw-6}" y="{y+sh_-6}" width="3" height="3" fill="{col}" class="gem" style="animation-delay:{i*.15:.2f}s"/>')
    b.append(text(code,x+sw/2,y+9,C['txt'],anchor='middle',shadow=C['sh']))
# cursor
cx,cy=pos[0]
cur=(f'<path d="M-2 -2h6v2h-4v4h-2zM{sw-4} -2h6v6h-2v-4h-4zM-2 {sh_-4}h2v4h4v2h-6zM{sw} {sh_-4}h2v6h-6v-2h4z" fill="{C["gold"]}"/>')
b.append(f'<g class="cur">{cur}</g>')
# tooltip panel
ty=gy+gh+10
b.append(window(6,ty,308,34))
N=len(items); T=1.3
for i,(code,full,cat) in enumerate(items):
    b.append(f'<g class="tip" style="animation-delay:{i*T:.2f}s">'
             +text('ITEM',16,ty+8,C['dim'])+text(full,64,ty+8,C['txt'])
             +text('TYPE',16,ty+20,C['dim'])+text(cat,64,ty+20,rar[cat])+'</g>')
kf=''.join(f'{i*100/N:.3f}%{{transform:translate({x}px,{y}px)}}' for i,(x,y) in enumerate(pos))
vis=100/N
style=f'''
.cur{{animation:cur {N*T}s steps(1) infinite}}@keyframes cur{{{kf}100%{{transform:translate({pos[0][0]}px,{pos[0][1]}px)}}}}
.tip{{opacity:0;animation:tip {N*T}s steps(1) infinite}}@keyframes tip{{0%{{opacity:1}}{vis:.3f}%{{opacity:0}}100%{{opacity:0}}}}
.gem{{animation:gm 2s steps(1) infinite}}@keyframes gm{{0%{{opacity:1}}50%{{opacity:.3}}}}
'''
open('assets/inventory.svg','w').write(svg(W,H,''.join(b),style,'Inventory: tech stack'))
