from card import *
for name,col in [('LINKEDIN','#7fd4ff'),('INSTAGRAM',C['pink']),('EMAIL',C['gold'])]:
    w=max(width(name)+24,56); h=18
    b=[f'<rect x="2" y="2" width="{w-2}" height="{h-2}" fill="{C["sh"]}"/>',
       f'<rect x="0" y="0" width="{w-2}" height="{h-2}" fill="{C["win"]}"/>',
       f'<path d="M1 0h{w-4}v1h-{w-4}zM1 {h-3}h{w-4}v1h-{w-4}zM0 1h1v{h-4}h-1zM{w-3} 1h1v{h-4}h-1z" fill="{col}"/>',
       f'<rect x="2" y="2" width="{w-6}" height="1" fill="#3e2e70"/>',
       f'<path class="a" d="M6 5h1v6h-1zM7 6h1v4h-1zM8 7h1v2h-1z" fill="{col}"/>',
       text(name,14,4,C['txt'],shadow=C['sh'])]
    st='.a{animation:bl 1s steps(1) infinite}@keyframes bl{0%{opacity:1}50%{opacity:0}}'
    open(f'assets/btn-{name.lower()}.svg','w').write(svg(w,h,''.join(b),st,name))
