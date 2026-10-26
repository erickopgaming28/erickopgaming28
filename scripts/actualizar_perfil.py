"""Ficha RPG del perfil: exclusivamente datos públicos y biblioteca estándar."""
from __future__ import annotations

import argparse
import base64
from datetime import datetime
from html import escape
import json
import os
from pathlib import Path
import urllib.request
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
USER = 'erickopgaming28'
THEMES = {
 'dark': dict(bg='#0b1720', panel='#11242a', ink='#e5f7e8', soft='#a6c5bb', line='#36554e', mint='#72edb3', gold='#ffd18a', blue='#a5ceff'),
 'light': dict(bg='#f5f8ef', panel='#eaf1e5', ink='#163b32', soft='#3d6156', line='#9aaf9d', mint='#146541', gold='#85510c', blue='#245c91'),
}
FONT = base64.b64encode((ROOT/'assets/fonts/PixelifySans.ttf').read_bytes()).decode('ascii')

def public_api(path: str):
 headers = {'User-Agent': 'erickopgaming28-profile', 'Accept': 'application/vnd.github+json'}
 token = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
 if token:
  headers['Authorization'] = 'Bearer '+token
 request = urllib.request.Request('https://api.github.com/'+path, headers=headers)
 with urllib.request.urlopen(request, timeout=30) as r:
  return json.load(r)

def fetch_stats():
 repos = []
 page = 1
 while True:
  rows = public_api(f'users/{USER}/repos?per_page=100&page={page}&type=owner')
  repos += [r for r in rows if not r.get('private',True) and not r.get('fork') and r['name'].lower()!=USER.lower()]
  if len(rows)<100:
   break
  page += 1
 stars = sum(r['stargazers_count'] for r in repos)
 languages = sorted({r['language'] for r in repos if r.get('language')})
 xp = 100*len(repos)+25*stars
 return dict(username=USER, repositories=sorted(r['name'] for r in repos), public_repos=len(repos), stars=stars,
             languages=languages, xp=xp, level=xp//100+1, level_progress=xp%100,
             next_level_xp=(xp//100+1)*100, updated=datetime.now(ZoneInfo('America/Mexico_City')).strftime('%Y-%m-%d'),
             formula='100 XP por repositorio público propio (sin este perfil ni forks) + 25 XP por estrella recibida')

class Drawing:
 def __init__(self,w,h,t,title,desc):
  self.w,self.h,self.t=w,h,t
  self.parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>',
   f'<style>@font-face{{font-family:Pixel;src:url(data:font/ttf;base64,{FONT}) format("truetype");font-weight:100 900}}text{{font-family:Pixel,monospace}}.flow{{stroke-dasharray:5 15;animation:travel 8s linear infinite}}@keyframes travel{{to{{stroke-dashoffset:-80}}}}@media(prefers-reduced-motion:reduce){{.flow{{animation:none}}}}</style>']
  self.rect(0,0,w,h,t['bg'])
 def rect(self,x,y,w,h,color,stroke=None):
  self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}"'+(f' stroke="{stroke}" stroke-width="2"' if stroke else '')+'/>')
 def text(self,x,y,value,size=28,color=None,anchor='start'):
  self.parts.append(f'<text x="{x}" y="{y}" fill="{color or self.t["ink"]}" font-size="{size}" text-anchor="{anchor}">{escape(str(value))}</text>')
 def path(self,d,color,width=2,cls=''):
  self.parts.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" class="{cls}"/>')
 def diamond(self,x,y,color,s=10):
  self.parts.append(f'<path d="M{x} {y-s}L{x+s} {y}L{x} {y+s}L{x-s} {y}Z" fill="{color}"/>')
 def save(self,path):
  path.parent.mkdir(parents=True,exist_ok=True)
  path.write_text(''.join(self.parts)+'</svg>\n',encoding='utf-8')

def player(stats,t):
 d=Drawing(840,292,t,'Ficha de jugador de Erick',f'Nivel {stats["level"]}, {stats["xp"]} XP, {stats["public_repos"]} repositorios públicos y {stats["stars"]} estrellas. Experiencia lúdica basada en datos públicos, no una valoración profesional.')
 d.path('M12 34V12H34 M806 12H828V34 M12 258V280H34 M806 280H828V258',t['line'],3)
 d.diamond(48,50,t['gold'],9)
 d.text(72,60,'ARTÍFICE DIGITAL',30,t['gold'])
 d.text(792,60,f'NV. {stats["level"]:02}',38,t['mint'],'end')
 d.text(38,118,f'{stats["xp"]} XP',48)
 d.text(798,116,f'PRÓXIMO NIVEL: {stats["next_level_xp"]}',26,t['soft'],'end')
 for i in range(40):
  d.rect(38+i*19.1,140,15.5,24,t['mint'] if i<(40*stats['level_progress']//100) else t['line'])
 d.text(38,218,f'{stats["public_repos"]:02} REPOS PÚBLICOS',27)
 d.text(798,218,f'{stats["stars"]:02} ESTRELLAS',27,t['gold'],'end')
 d.text(38,260,'GUARDADO: '+stats['updated'],23,t['soft'])
 d.text(798,260,f'{stats["next_level_xp"]-stats["xp"]} XP PARA SUBIR',23,t['soft'],'end')
 return d

BRANCHES=[
 ('ARCANISTA','IA Y DATOS','Python','SQLite · PySide6','AI Token Monitor','blue'),
 ('BARDO','MÚSICA Y WEB','JavaScript','Node.js · Spotify API','Clasificador de Música','mint'),
 ('ARTÍFICE','DEL CÓDIGO AL PAPEL','Python · SVG','Bambu Lab A1','Pluma A1','gold'),
]

def tree(t,mobile=False):
 w,h=(420,835) if mobile else (840,440)
 d=Drawing(w,h,t,'Árbol de habilidades: Arcanista, Bardo y Artífice','Tres caminos basados en tecnologías de proyectos públicos: IA y datos con Python, SQLite y PySide6; música y web con JavaScript, Node.js y Spotify API; código al papel con Python, SVG y Bambu Lab A1.')
 if mobile:
  d.diamond(37,53,t['mint'],12)
  d.text(65,62,'CREAR ALGO ÚTIL',29)
  d.path('M37 78V757',t['line'],3)
  d.path('M37 78V757',t['mint'],3,'flow')
  for i,(name,role,tech,more,project,c) in enumerate(BRANCHES):
   y=123+i*225
   d.diamond(37,y+30,t[c],9)
   d.path(f'M49 {y+30}H71',t[c],2)
   d.rect(72,y,324,188,t['panel'],t['line'])
   d.text(92,y+39,name,35,t[c])
   d.text(92,y+70,role,21,t['soft'])
   d.text(92,y+109,tech,28)
   d.text(92,y+141,more,23,t['soft'])
   d.text(92,y+171,project,23,t[c])
 else:
  d.diamond(420,38,t['mint'],12)
  d.text(420,91,'CREAR ALGO ÚTIL',35,anchor='middle')
  d.path('M420 111V140 M145 140H695 M145 140V176 M420 140V176 M695 140V176',t['line'],3)
  d.path('M145 140H695',t['mint'],3,'flow')
  for i,(name,role,tech,more,project,c) in enumerate(BRANCHES):
   x=24+i*275
   d.diamond(x+121,173,t[c],8)
   d.rect(x,196,242,216,t['panel'],t['line'])
   d.text(x+20,238,name,35,t[c])
   d.text(x+20,270,role,20,t['soft'])
   d.text(x+20,313,tech,28)
   d.text(x+20,345,more,21,t['soft'])
   # El proyecto se enlaza desde el diario de misiones del README.
   d.text(x+20,386,['DATOS → DECISIONES','SONIDO → PLAYLISTS','IDEAS → TRAZOS'][i],21,t[c])
 return d

def update_readme(stats):
 p=ROOT/'README.md'; text=p.read_text(encoding='utf-8')
 first='<!-- PLAYER:START -->';last='<!-- PLAYER:END -->'
 replacement=f'\n**Nivel {stats["level"]:02} · {stats["xp"]} XP** · {stats["public_repos"]} repositorios públicos · {stats["stars"]} estrella'+('s' if stats['stars']!=1 else '')+f' recibida'+('s' if stats['stars']!=1 else '')+f'. Faltan **{stats["next_level_xp"]-stats["xp"]} XP** para el nivel {stats["level"]+1:02}.\n'
 before,rest=text.split(first,1);_,after=rest.split(last,1)
 p.write_text(before+first+replacement+last+after,encoding='utf-8')

def main():
 args=argparse.ArgumentParser()
 args.add_argument('--desde',type=Path,help='Reutilizar una captura pública para renderizar sin red.')
 ns=args.parse_args()
 stats=json.loads(ns.desde.read_text(encoding='utf-8')) if ns.desde else fetch_stats()
 if not stats.get('repositories') or any('/' in name for name in stats['repositories']):
  raise ValueError('Captura pública inválida')
 for name,t in THEMES.items():
  player(stats,t).save(ROOT/f'assets/jugador-{name}.svg')
  tree(t).save(ROOT/f'assets/habilidades-{name}.svg')
  tree(t,True).save(ROOT/f'assets/habilidades-mobile-{name}.svg')
 (ROOT/'assets/progreso.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 update_readme(stats)
 print(f'Perfil: nivel {stats["level"]}, {stats["xp"]} XP; solo {stats["public_repos"]} repositorios públicos.')

if __name__=='__main__':
 main()
