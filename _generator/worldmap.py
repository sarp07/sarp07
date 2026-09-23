import os, sys, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from card import *
from global_land_mask import globe  # pip install global-land-mask pillow
W=320
LON0,LON1,LAT0,LAT1=-25,185,72,-50
MX,MY,MW=10,20,300
CELL=2
cols=MW//CELL
deg=(LON1-LON0)/cols
rows=int((LAT0-LAT1)/deg)
MH=rows*CELL
def ll2xy(lat,lon):
    return MX+(lon-LON0)/deg*CELL, MY+(LAT0-lat)/deg*CELL
def land(lat,lon):
    lon2=lon-360 if lon>180 else lon
    return globe.is_land(lat,lon2)
cells=[]
for r in range(rows):
    for c in range(cols):
        lat=LAT0-(r+.5)*deg; lon=LON0+(c+.5)*deg
        # majority of 4 samples
        n=sum(land(lat+dy*deg/4,lon+dx*deg/4) for dx in(-1,1) for dy in(-1,1))
        if n>=2: cells.append((c,r))
cs=set(cells)
realms=[
 ('TURKIYE',36.9,30.7,'HOME BASE',['CRYPTO EXCHANGE, CHAIN FORK','TG MINI APPS + GAME, DEFI','NFT MARKET, FEE REBATES']),
 ('ALBANIA',41.3,19.8,'EUROPE',['PERP DEX','MULTI DEFI APP']),
 ('LONDON, UK',51.5,-0.1,'EUROPE',['L2 CHAIN ARCHITECTURE','CHAIN OPS + MANAGEMENT']),
 ('DUBAI, UAE',25.2,55.3,'MIDDLE EAST',['COPY TRADE PLATFORM','PERP DEX']),
 ('QATAR',25.3,51.5,'MIDDLE EAST',['MEMECOIN PROJECT','']),
 ('INDONESIA',-6.2,106.8,'ASIA',['TELEGRAM MINI APP','']),
 ('NEW ZEALAND',-41.3,174.8,'OCEANIA',['TELEGRAM MINI APP','']),
]
TY=MY+MH+12
H=TY+62+6
b=[f'<rect width="{W}" height="{H}" fill="{C["bg"]}"/>']
b.append(window(4,MY-10,312,MH+18,'WORLD MAP'))
_t='7 REALMS, 3 CONTINENTS'
b.append(f'<rect x="{308-width(_t)-8}" y="{MY-14}" width="{width(_t)+8}" height="9" fill="{C["sh"]}"/>')
b.append(text(_t,304,MY-13,C['gold'],anchor='end'))
# sea with graticule dots
b.append(f'<rect x="{MX}" y="{MY}" width="{MW}" height="{MH}" fill="#140d2c"/>')
gr=[]
for lon in range(-20,181,20):
    x,_=ll2xy(0,lon)
    gr+= [(int(x),y) for y in range(MY,MY+MH,4)]
for lat in range(-40,71,20):
    _,y=ll2xy(lat,0)
    gr+= [(x,int(y)) for x in range(MX,MX+MW,4)]
b.append(f'<path d="{rects_path(gr)}" fill="#2a2052"/>')
# land
full=[(MX+c*CELL+dx,MY+r*CELL+dy) for c,r in cells for dx in range(CELL) for dy in range(CELL)]
b.append(f'<path d="{rects_path(full)}" fill="#3e2f70"/>')
coast=[(MX+c*CELL+dx,MY+r*CELL) for c,r in cells if (c,r-1) not in cs for dx in range(CELL)]
b.append(f'<path d="{rects_path(coast)}" fill="#6a58a8"/>')
shade=[(MX+c*CELL+dx,MY+r*CELL+CELL-1) for c,r in cells if (c,r+1) not in cs for dx in range(CELL)]
b.append(f'<path d="{rects_path(shade)}" fill="#2a1f52"/>')
# routes from home
hx,hy=ll2xy(36.9,30.7)
k=0
for name,lat,lon,*_ in realms[1:]:
    x,y=ll2xy(lat,lon)
    mx,my=(hx+x)/2,(hy+y)/2-max(8,math.hypot(x-hx,y-hy)*0.25)
    L=math.hypot(x-hx,y-hy); n=max(3,int(L/3))
    for i in range(1,n):
        t=i/n; px=(1-t)**2*hx+2*(1-t)*t*mx+t*t*x; py=(1-t)**2*hy+2*(1-t)*t*my+t*t*y
        b.append(f'<rect class="rt" style="animation-delay:{(i/n)*2:.2f}s" x="{int(px)}" y="{int(py)}" width="1" height="1" fill="{C["org"]}"/>')
# pins
pos=[]
for i,(name,lat,lon,*_) in enumerate(realms):
    x,y=ll2xy(lat,lon); x,y=int(x),int(y); pos.append((x,y))
    if i==0:
        castle=["G.G.G","GGGGG",".GYG.",".GGG."]
        b.append(f'<g class="ring" style="transform-origin:{x}px {y}px"><rect x="{x-5}" y="{y-5}" width="11" height="11" fill="none" stroke="{C["gold"]}" stroke-width="1"/></g>')
        b.append(sprite(castle,x-2,y-2,{'G':C['gold'],'Y':C['sh']}))
    else:
        b.append(f'<g class="ring" style="animation-delay:{i*.3:.1f}s;transform-origin:{x}px {y}px"><rect x="{x-4}" y="{y-4}" width="9" height="9" fill="none" stroke="{C["pink"]}" stroke-width="1"/></g>')
        b.append(f'<rect x="{x-1}" y="{y-1}" width="3" height="3" fill="#fff4d6"/><rect x="{x}" y="{y}" width="1" height="1" fill="{C["pink"]}"/>')
# cursor
cur='<path d="M-6 -6h3v1h-2v2h-1zM4 -6h3v3h-1v-2h-2zM-6 4h1v2h2v1h-3zM6 4h1v3h-3v-1h2z" fill="#7cf2a0"/>'
b.append(f'<g class="cur">{cur}</g>')
# tooltip
b.append(window(4,TY,312,62))
N=len(realms); T=2.4
for i,(name,lat,lon,region,q) in enumerate(realms):
    g=text('REALM',14,TY+7,C['dim'])+text(name,62,TY+7,C['txt'],shadow=C['sh'])+text(region,306,TY+7,C['gold'],anchor='end')
    g+=text('QUEST',14,TY+20,C['dim'])+text(q[0],62,TY+20,'#7cf2a0')
    for j,l in enumerate(q[1:]):
        if l: g+=text(l,62,TY+32+12*j,'#7cf2a0')
    b.append(f'<g class="tip" style="animation-delay:{i*T:.1f}s">{g}</g>')
kf=''.join(f'{i*100/N:.3f}%{{transform:translate({x}px,{y}px)}}' for i,(x,y) in enumerate(pos))
style=f'''
.rt{{animation:rt 2s steps(2) infinite}}@keyframes rt{{0%,100%{{opacity:.25}}50%{{opacity:1}}}}
.ring{{animation:ring 1.6s steps(4) infinite}}@keyframes ring{{0%{{transform:scale(.4);opacity:1}}100%{{transform:scale(1.4);opacity:0}}}}
.cur{{animation:cur {N*T}s steps(1) infinite}}@keyframes cur{{{kf}100%{{transform:translate({pos[0][0]}px,{pos[0][1]}px)}}}}
.tip{{opacity:0;animation:tip {N*T}s steps(1) infinite}}@keyframes tip{{0%{{opacity:1}}{100/N:.3f}%{{opacity:0}}100%{{opacity:0}}}}
'''
open(sys.argv[1] if len(sys.argv)>1 else 'assets/worldmap.svg','w').write(svg(W,H,''.join(b),style,'World map: Turkiye, Albania, London, Dubai, Qatar, Indonesia, New Zealand'))
print(rows,MH,H)
