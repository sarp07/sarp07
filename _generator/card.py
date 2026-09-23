from common import *
C=dict(bg='#1b1236',win='#2a1d52',win2='#231847',bd='#fff4d6',bd2='#9a7ac8',gold='#ffd36b',org='#f7964c',pink='#e8705a',txt='#fff4d6',dim='#b9a6e0',sh='#0e0820')
def window(x,y,w,h,title=None):
    s=[f'<rect x="{x+2}" y="{y+2}" width="{w}" height="{h}" fill="{C["sh"]}"/>',
       f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{C["win"]}"/>',
       f'<rect x="{x}" y="{y+h//2}" width="{w}" height="{h-h//2}" fill="{C["win2"]}"/>',
       f'<path d="M{x+1} {y}h{w-2}v1h-{w-2}zM{x+1} {y+h-1}h{w-2}v1h-{w-2}zM{x} {y+1}h1v{h-2}h-1zM{x+w-1} {y+1}h1v{h-2}h-1z" fill="{C["bd"]}"/>',
       f'<path d="M{x+2} {y+2}h{w-4}v1h-{w-4}zM{x+2} {y+h-3}h{w-4}v1h-{w-4}zM{x+2} {y+3}h1v{h-6}h-1zM{x+w-3} {y+3}h1v{h-6}h-1z" fill="{C["bd2"]}"/>']
    if title:
        tw=width(title)+8
        s.append(f'<rect x="{x+8}" y="{y-4}" width="{tw}" height="9" fill="{C["org"]}"/>')
        s.append(f'<rect x="{x+8}" y="{y+4}" width="{tw}" height="1" fill="{C["sh"]}"/>')
        s.append(text(title,x+12,y-3,C['sh']))
    return ''.join(s)
