"""Exporta un GIF del paisaje con partículas propias; conserva el PNG original.

Requiere Pillow y FFmpeg. Pillow dibuja únicamente una capa geométrica
transparente; FFmpeg compone y codifica la secuencia de vídeo.
"""
from pathlib import Path
import math
import shutil
import subprocess

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
FRAMES = ROOT/'local/particulas'
FPS, COUNT = 12, 72
W, H = 840, 280


def square(draw, x, y, color, size=2):
 x, y = round(x), round(y)
 draw.rectangle((x,y,x+size-1,y+size-1), fill=color)


def main():
 ffmpeg = shutil.which('ffmpeg')
 if not ffmpeg:
  raise SystemExit('Falta FFmpeg en PATH.')
 FRAMES.mkdir(parents=True,exist_ok=True)
 for frame in range(COUNT):
  phase = frame/COUNT*math.tau
  layer = Image.new('RGBA',(W,H),(0,0,0,0))
  draw = ImageDraw.Draw(layer)
  # Luciérnagas del bosque: un recorrido periódico, lento y sin cortes.
  for i in range(28):
   x = 28+(i*79)%780 + math.sin(phase+i*1.7)*7
   y = 173+(i*31)%95 + math.cos(phase+i*.83)*9
   alpha = int(105+65*math.sin(phase+i*1.31))
   square(draw,x-1,y-1,(80,230,181,alpha//5),5)
   square(draw,x,y,(154,255,219,alpha),2)
  # Estrellas: variaciones graduales, sin parpadear el texto.
  for i,(x,y) in enumerate([(410,18),(492,44),(555,11),(710,23),(807,49),(354,32)]):
   alpha=int(100+70*math.cos(phase+i))
   square(draw,x-3,y,(194,234,255,alpha),7)
   draw.rectangle((x,y-3,x+1,y+4),fill=(194,234,255,alpha))
  # Pequeñas chispas de magia acompañan los tres destinos del mapa.
  for j,(cx,cy) in enumerate([(354,143),(551,101),(765,120)]):
   for k in range(3):
    angle=phase+k*math.tau/3+j
    x=cx+math.cos(angle)*17
    y=cy+math.sin(angle)*9
    square(draw,x,y,(255,211,135,170),2)
  # Reflejos cortos sobre el agua, sin deformar la ilustración.
  for i in range(8):
   x=145+i*31+math.sin(phase+i)*4
   y=224+(i*7)%24
   a=int(35+30*(1+math.sin(phase+i))*.5)
   draw.rectangle((round(x),y,round(x)+5,y),fill=(148,255,220,a))
  layer.save(FRAMES/f'{frame:03}.png')
 target=ROOT/'assets/aventura-viva.gif'
 graph='[0:v]scale=840:280:flags=lanczos[base];[base][1:v]overlay=shortest=1:format=auto,fps=12,split[a][b];[a]palettegen=max_colors=192:stats_mode=full[p];[b][p]paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle[out]'
 cmd=[ffmpeg,'-hide_banner','-loglevel','error','-y','-loop','1','-i',str(ROOT/'assets/aventura.png'),'-framerate',str(FPS),'-i',str(FRAMES/'%03d.png'),'-filter_complex',graph,'-map','[out]','-t',str(COUNT/FPS),'-an','-loop','0',str(target)]
 subprocess.run(cmd,check=True)
 with Image.open(target) as result:
  assert result.is_animated and result.n_frames>30
  print(f'GIF: {result.size}, {result.n_frames} cuadros, {target.stat().st_size:,} bytes')


if __name__=='__main__':
 main()
