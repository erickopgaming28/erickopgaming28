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
 'dark': dict(bg='#0b1720', panel='#11242a', ink='#e5f7e8', soft='#a6c5bb', line='#36554e', mint='#9ed9bd', gold='#e4c699', blue='#b4c9e3'),
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
   f'<style>@font-face{{font-family:Pixel;src:url(data:font/ttf;base64,{FONT}) format("truetype");font-weight:100 900}}text{{font-family:Pixel,monospace}}</style>']
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
 d=Drawing(640,100,t,'Nivel y experiencia de Erick',f'Nivel {stats["level"]}, {stats["xp"]} XP. Faltan {stats["next_level_xp"]-stats["xp"]} XP para subir. Progreso lúdico basado en datos públicos.')
 d.diamond(24,26,t['mint'],5)
 d.text(40,34,f'NIVEL {stats["level"]:02}',25,t['mint'])
 d.text(620,34,f'{stats["xp"]} XP',25,t['ink'],'end')
 for i in range(40):
  d.rect(20+i*15.1,49,12,10,t['mint'] if i<(40*stats['level_progress']//100) else t['line'])
 d.text(320,86,f'{stats["next_level_xp"]-stats["xp"]} XP PARA NIVEL {stats["level"]+1:02}',22,t['soft'],'middle')
 return d

BRANCHES=[
 ('ARCANISTA','IA Y DATOS','Python','SQLite · PySide6','AI Token Monitor','blue'),
 ('BARDO','MÚSICA Y WEB','JavaScript','Node.js · Spotify API','Clasificador de Música','mint'),
 ('ARTÍFICE','DEL CÓDIGO AL PAPEL','Python · SVG','Bambu Lab A1','Pluma A1','gold'),
]

def tree(t,mobile=False):
 w,h=(420,505) if mobile else (720,270)
 d=Drawing(w,h,t,'Árbol de habilidades: Arcanista, Bardo y Artífice','Tres caminos basados en tecnologías de proyectos públicos: IA y datos con Python, SQLite y PySide6; música y web con JavaScript, Node.js y Spotify API; código al papel con Python, SVG y Bambu Lab A1.')
 if mobile:
  d.diamond(30,32,t['mint'],6)
  d.text(56,40,'CREAR ALGO ÚTIL',25)
  d.path('M30 44V427',t['line'],2)
  for i,(name,role,tech,more,project,c) in enumerate(BRANCHES):
   y=80+i*141
   d.diamond(30,y+14,t[c],5)
   d.path(f'M36 {y+14}H56',t['line'],2)
   d.text(70,y+24,name,27,t[c])
   d.text(70,y+53,role,20,t['soft'])
   d.text(70,y+85,tech,23)
   d.text(70,y+113,more,21,t['soft'])
 else:
  d.diamond(360,26,t['mint'],6)
  d.text(360,61,'CREAR ALGO ÚTIL',25,anchor='middle')
  d.path('M360 76V94 M120 94H600 M120 94V118 M360 94V118 M600 94V118',t['line'],2)
  for i,(name,role,tech,more,project,c) in enumerate(BRANCHES):
   x=120+i*240
   d.diamond(x,119,t[c],5)
   d.text(x,158,name,28,t[c],'middle')
   d.text(x,186,role,18,t['soft'],'middle')
   d.text(x,221,tech,23,anchor='middle')
   d.text(x,249,more,19,t['soft'],'middle')
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
