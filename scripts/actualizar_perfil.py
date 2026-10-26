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
   f'<style>@font-face{{font-family:Pixel;src:url(data:font/ttf;base64,{FONT}) format("truetype");font-weight:100 900}}text{{font-family:Pixel,monospace}}.rune{{animation:breathe 4s ease-in-out infinite}}.ember{{animation:float 3s ease-in-out infinite}}.trail{{animation:shimmer 6s linear infinite}}@keyframes breathe{{0%,100%{{opacity:.55}}50%{{opacity:1}}}}@keyframes float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-3px)}}}}@keyframes shimmer{{0%{{opacity:0;transform:translateX(0)}}20%,75%{{opacity:.55}}100%{{opacity:0;transform:translateX(125px)}}}}@media(prefers-reduced-motion:reduce){{.rune,.ember,.trail{{animation:none}}.trail{{opacity:0}}}}</style>']
  self.rect(0,0,w,h,t['bg'])
 def rect(self,x,y,w,h,color,stroke=None):
  self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}"'+(f' stroke="{stroke}" stroke-width="2"' if stroke else '')+'/>')
 def text(self,x,y,value,size=28,color=None,anchor='start'):
  self.parts.append(f'<text x="{x}" y="{y}" fill="{color or self.t["ink"]}" font-size="{size}" text-anchor="{anchor}">{escape(str(value))}</text>')
 def path(self,d,color,width=2,cls=''):
  self.parts.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" class="{cls}"/>')
 def diamond(self,x,y,color,s=10,cls=''):
  self.parts.append(f'<path class="{cls}" d="M{x} {y-s}L{x+s} {y}L{x} {y+s}L{x-s} {y}Z" fill="{color}"/>')
 def save(self,path):
  path.parent.mkdir(parents=True,exist_ok=True)
  path.write_text(''.join(self.parts)+'</svg>\n',encoding='utf-8')

def player(stats,t):
 d=Drawing(640,100,t,'Nivel y experiencia de Erick',f'Nivel {stats["level"]}, {stats["xp"]} XP. Faltan {stats["next_level_xp"]-stats["xp"]} XP para subir. Progreso lúdico basado en datos públicos.')
 d.diamond(24,26,t['mint'],5,'rune')
 d.text(40,34,f'NIVEL {stats["level"]:02}',25,t['mint'])
 d.text(620,34,f'{stats["xp"]} XP',25,t['ink'],'end')
 for i in range(40):
  d.rect(20+i*15.1,49,12,10,t['mint'] if i<(40*stats['level_progress']//100) else t['line'])
 # Un brillo recorre solo la parte ya ganada. Las cifras nunca se animan.
 earned = 40*stats['level_progress']//100
 if earned:
  limit=max(0,earned*15.1-3)
  d.parts.append(f'<defs><clipPath id="earned"><rect x="20" y="49" width="{limit}" height="10"/></clipPath></defs><g clip-path="url(#earned)"><rect class="trail" x="20" y="49" width="14" height="10" fill="{t["ink"]}"/></g>')
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
  d.diamond(30,32,t['mint'],6,'rune')
  d.text(56,40,'CREAR ALGO ÚTIL',25)
  d.path('M30 44V427',t['line'],2)
  for i,(name,role,tech,more,project,c) in enumerate(BRANCHES):
   y=80+i*141
   d.diamond(30,y+14,t[c],5,'rune')
   d.path(f'M36 {y+14}H56',t['line'],2)
   d.text(70,y+24,name,27,t[c])
   d.text(70,y+53,role,20,t['soft'])
   d.text(70,y+85,tech,23)
   d.text(70,y+113,more,21,t['soft'])
 else:
  d.diamond(360,26,t['mint'],6,'rune')
  d.text(360,61,'CREAR ALGO ÚTIL',25,anchor='middle')
  d.path('M360 76V94 M120 94H600 M120 94V118 M360 94V118 M600 94V118',t['line'],2)
  for i,(name,role,tech,more,project,c) in enumerate(BRANCHES):
   x=120+i*240
   d.diamond(x,119,t[c],5,'rune')
   d.text(x,158,name,28,t[c],'middle')
   d.text(x,186,role,18,t['soft'],'middle')
   d.text(x,221,tech,23,anchor='middle')
   d.text(x,249,more,19,t['soft'],'middle')
 return d

def achievement(t,title,caption,kind,unlocked):
 d=Drawing(220,70,t,title,caption)
 c=t[kind] if unlocked else t['soft']
 d.diamond(20,23,c,6)
 d.text(37,30,title,23,c)
 d.text(20,57,caption,18,t['soft'])
 return d

def camp(t):
 d=Drawing(640,82,t,'El campamento de ideas','Una pequeña hoguera animada acompaña la frase: aprender, construir, mejorar.')
 # Hoguera: icono de geometría propia a escala pequeña.
 d.parts.append('<g class="ember">')
 d.rect(30,39,22,8,t['gold'])
 d.rect(34,29,14,14,t['gold'])
 d.rect(38,23,6,12,t['gold'])
 d.rect(38,38,6,10,t['ink'])
 d.parts.append('</g>')
 d.path('M27 58H55 M31 64H51',t['soft'],3)
 d.text(78,37,'EN EL CAMPAMENTO',24,t['gold'])
 d.text(78,64,'Aprender, construir, mejorar.',22,t['soft'])
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
  achievement(t,'EXPLORADOR',f'{stats["public_repos"]} repos públicos','mint',stats['public_repos']>=1).save(ROOT/f'assets/logro-explorador-{name}.svg')
  achievement(t,'MULTICLASE',f'{len(stats["languages"])} lenguajes','blue',len(stats['languages'])>=2).save(ROOT/f'assets/logro-multiclase-{name}.svg')
  achievement(t,'ESTRELLA',f'{stats["stars"]} recibida'+('s' if stats['stars']!=1 else ''),'gold',stats['stars']>=1).save(ROOT/f'assets/logro-estrella-{name}.svg')
  camp(t).save(ROOT/f'assets/campamento-{name}.svg')
 (ROOT/'assets/progreso.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 update_readme(stats)
 print(f'Perfil: nivel {stats["level"]}, {stats["xp"]} XP; solo {stats["public_repos"]} repositorios públicos.')

if __name__=='__main__':
 main()
