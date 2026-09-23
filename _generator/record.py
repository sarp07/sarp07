"""Generates assets/record.svg (pixel PLAYER RECORD card).
Runs in GitHub Actions: needs env GH_TOKEN and GH_USER."""
import os, sys, json, urllib.request, datetime
sys.path.insert(0, os.path.dirname(__file__))
from card import *

def gql(q, v, tok):
    req = urllib.request.Request('https://api.github.com/graphql',
        data=json.dumps({'query': q, 'variables': v}).encode(),
        headers={'Authorization': f'bearer {tok}', 'Content-Type': 'application/json'})
    return json.load(urllib.request.urlopen(req))['data']

def fetch(user, tok):
    q = '''query($u:String!,$c:String){user(login:$u){
      followers{totalCount}
      contributionsCollection{totalCommitContributions restrictedContributionsCount
        totalPullRequestContributions totalIssueContributions
        contributionCalendar{totalContributions}}
      repositories(first:100,after:$c,ownerAffiliations:OWNER,isFork:false){
        totalCount pageInfo{hasNextPage endCursor} nodes{stargazerCount}}}}'''
    stars = 0; cur = None
    while True:
        d = gql(q, {'u': user, 'c': cur}, tok)['user']
        r = d['repositories']; stars += sum(n['stargazerCount'] for n in r['nodes'])
        if not r['pageInfo']['hasNextPage']: break
        cur = r['pageInfo']['endCursor']
    c = d['contributionsCollection']
    return dict(stars=stars, commits=c['totalCommitContributions'] + c['restrictedContributionsCount'],
                prs=c['totalPullRequestContributions'], issues=c['totalIssueContributions'],
                repos=r['totalCount'], contribs=c['contributionCalendar']['totalContributions'],
                followers=d['followers']['totalCount'])

def render(s, out):
    W, H = 250, 110
    b = [f'<rect width="{W}" height="{H}" fill="{C["bg"]}"/>']
    b.append(window(4, 10, 242, 94, 'PLAYER RECORD'))
    rows = [('STARS', s['stars'], C['gold']), ('COMMITS', s['commits'], C['org']),
            ('PULL REQS', s['prs'], '#7cf2a0'), ('ISSUES', s['issues'], C['pink']),
            ('REPOS', s['repos'], '#7fd4ff'), ('CONTRIBS', s['contribs'], '#c9a0ff')]
    for i, (k, v, c) in enumerate(rows):
        y = 22 + i * 11
        b.append(f'<rect x="12" y="{y+1}" width="5" height="5" fill="{c}"/>')
        b.append(text(k, 22, y, C['dim']))
        b.append(text(f'{v:,}' if isinstance(v,int) else str(v), 170, y, C['txt'], anchor='end', shadow=C['sh']))
    b.append(text('LAST 12 MONTHS', 12, 93, '#6a5a9a'))
    # spinning coin
    f1 = ["..GGGG..", ".GYYYYG.", "GYYGGYYG", "GYGYYGYG", "GYGYYGYG", "GYYGGYYG", ".GYYYYG.", "..GGGG.."]
    f2 = ["...GG...", "..GYYG..", "..GYYG..", "..GYGG..", "..GYGG..", "..GYYG..", "..GYYG..", "...GG..."]
    f3 = ["...GG...", "...GG...", "...GG...", "...GG...", "...GG...", "...GG...", "...GG...", "...GG..."]
    pal = {'G': '#c98a2a', 'Y': C['gold']}
    coin = ''.join(f'<g class="k{i}" transform="translate(196 34) scale(4)">{sprite(fr,0,0,pal)}</g>' for i, fr in enumerate([f1, f2, f3, f2]))
    b.append(f'<rect x="192" y="68" width="40" height="3" fill="{C["sh"]}"/>')
    b.append(f'<g class="hop">{coin}</g>')
    b.append(text(f'x{s["followers"]}', 212, 76, C['txt'], anchor='middle'))
    b.append(text('ALLIES', 212, 88, C['dim'], anchor='middle'))
    style = ''.join(f'.k{i}{{opacity:0;animation:k 1.2s steps(1) infinite;animation-delay:{i*0.3}s}}' for i in range(4))
    style += '@keyframes k{0%{opacity:1}25%{opacity:0}}.hop{animation:hop 1.2s steps(1) infinite}@keyframes hop{0%{transform:translateY(0)}50%{transform:translateY(-2px)}}'
    open(out, 'w').write(svg(W, H, ''.join(b), style, 'Player record: GitHub stats'))

if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else 'assets/record.svg'
    tok = os.environ.get('GH_TOKEN')
    s = fetch(os.environ.get('GH_USER', 'sarp07'), tok) if tok else \
        {k: '?' for k in ['stars','commits','prs','issues','repos','contribs','followers']}
    print(s); render(s, out)
