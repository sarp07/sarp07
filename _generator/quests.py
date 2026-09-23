from card import *
import random
W=320
main=[('FAINERA FEE','CRYPTO TRADING FEE REBATES','LIVE','#7cf2a0'),
      ('FAINERA TRADE','COPY TRADE SOCIAL NETWORK','ACTIVE',C['gold']),
      ('PURPDEX','PERP DEX ON BNB CHAIN, 100X','LIVE','#7cf2a0'),
      ('SHIT TO EARN','SOCIALFI GAME ON ROBINHOOD CHAIN','IN DEV',C['pink'])]
done=[('AGRO WALLET','WALLET + EXTENSION'),('NFT MARKET V3','NFT MARKETPLACE'),('METACYBER','NFT CARD BATTLE GAME'),('FARMER GAME','P2E NFT STAKING')]
y0=14
mh=len(main)*22+10
dh=len(done)*12+12
H=y0+mh+14+dh+8
b=[f'<rect width="{W}" height="{H}" fill="{C["bg"]}"/>']
random.seed(9)
b.append(f'<path d="{rects_path([(random.randint(0,W-1),random.randint(0,H-1)) for _ in range(90)])}" fill="#3a2a66"/>')
b.append(window(6,y0-4,308,mh,'MAIN QUESTS'))
bang=["..GG..","..GG..","..GG..","..GG..","......","..GG.."]
for i,(n,d,st,c) in enumerate(main):
    y=y0+6+i*22
    b.append(f'<g class="bang" style="animation-delay:{i*.2}s">{sprite(bang,19,y,{"G":C["gold"]})}</g>')
    b.append(text(n,30,y,C['txt'],shadow=C['sh']))
    b.append(text(d,30,y+10,C['dim']))
    tw=width(st)+6
    b.append(f'<rect x="{306-tw}" y="{y-2}" width="{tw}" height="11" fill="{c}"/>')
    b.append(f'<rect x="{306-tw}" y="{y+8}" width="{tw}" height="1" fill="{C["sh"]}"/>')
    b.append(text(st,306-tw+3,y,C['sh']))
    if i<len(main)-1:
        b.append(f'<path d="{rects_path([(x,y+19) for x in range(16,304,2)])}" fill="#4a3a7a"/>')
# selector arrow cycling
arrow=f'<path d="M10 0h1v7h-1zM11 1h1v5h-1zM12 2h1v3h-1zM13 3h1v1h-1z" fill="{C["org"]}"/>'
b.append(f'<g class="sel">{arrow}</g>')
y1=y0+mh+10
b.append(window(6,y1,308,dh,'CLEARED'))
chk=[".....G","....GG","G..GG.","GGGG..",".GG..."]
for i,(n,d) in enumerate(done):
    y=y1+9+i*12
    b.append(sprite(chk,14,y+1,{'G':'#7cf2a0'}))
    b.append(text(n,26,y,C['txt'])); b.append(text(d,138,y,C['dim']))
ys=[y0+6+i*22 for i in range(len(main))]
kf=''.join(f'{int(i*100/len(ys))}%{{transform:translateY({ys[i]}px)}}' for i in range(len(ys)))
style=f'''
.sel{{animation:sel 6s steps(1) infinite}}@keyframes sel{{{kf}100%{{transform:translateY({ys[0]}px)}}}}
.bang{{animation:bg 1s steps(1) infinite}}@keyframes bg{{0%{{transform:translateY(0)}}50%{{transform:translateY(-1px)}}}}
'''
open('assets/quests.svg','w').write(svg(W,H,''.join(b),style,'Quest log: FainEra Fee, FainEra Trade, PurpDex, Shit to Earn and cleared projects'))
