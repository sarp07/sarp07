from PIL import Image, ImageDraw, ImageFont
import os
FONT = ImageFont.truetype(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'PressStart2P.ttf'), 8)
_cache = {}
def bitmap(text):
    if text in _cache: return _cache[text]
    w = 8*len(text)+8
    img = Image.new('1', (w, 10), 0)
    d = ImageDraw.Draw(img); d.fontmode = '1'
    d.text((0,0), text, font=FONT, fill=1)
    px = img.load()
    pts = [(x,y) for y in range(10) for x in range(w) if px[x,y]]
    _cache[text]=pts; return pts
def width(text, s=1): return 8*len(text)*s
def path_d(text, x0, y0, s=1):
    # merge horizontal runs
    pts = set(bitmap(text)); rows={}
    for (x,y) in pts: rows.setdefault(y,[]).append(x)
    out=[]
    for y,xs in rows.items():
        xs.sort(); start=prev=xs[0]
        for x in xs[1:]+[None]:
            if x is not None and x==prev+1: prev=x; continue
            out.append(f"M{x0+start*s:g} {y0+y*s:g}h{(prev-start+1)*s:g}v{s:g}h{-(prev-start+1)*s:g}z")
            if x is not None: start=prev=x
    return ''.join(out)
def text(t, x, y, fill, s=1, cls='', anchor='start', shadow=None, extra=''):
    if anchor=='middle': x = x - width(t,s)/2
    elif anchor=='end': x = x - width(t,s)
    c = f' class="{cls}"' if cls else ''
    sh = f'<path d="{path_d(t,x+s,y+s,s)}" fill="{shadow}"/>' if shadow else ''
    return f'<g{c}{extra}>{sh}<path d="{path_d(t,x,y,s)}" fill="{fill}"/></g>'
