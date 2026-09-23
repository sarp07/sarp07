import random
from pixfont import text, width, path_d
def rects_path(cells):
    """cells: iterable of (x,y) unit pixels -> merged path"""
    rows={}
    for x,y in cells: rows.setdefault(y,set()).add(x)
    out=[]
    for y in sorted(rows):
        xs=sorted(rows[y]); start=prev=xs[0]
        for x in xs[1:]+[None]:
            if x is not None and x==prev+1: prev=x; continue
            out.append(f"M{start} {y}h{prev-start+1}v1h{-(prev-start+1)}z")
            if x is not None: start=prev=x
    return ''.join(out)
def sprite(rows, x0, y0, palette):
    """rows: list of strings; palette: char->color. returns svg paths"""
    by={}
    for j,r in enumerate(rows):
        for i,ch in enumerate(r):
            if ch in palette: by.setdefault(ch,[]).append((x0+i,y0+j))
    return ''.join(f'<path d="{rects_path(c)}" fill="{palette[k]}"/>' for k,c in by.items())
def svg(w,h,body,style='',title=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w*3}" height="{h*3}" '
            f'shape-rendering="crispEdges" role="img" aria-label="{title}"><title>{title}</title>'
            f'<style>{style}</style>{body}</svg>')
