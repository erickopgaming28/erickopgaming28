# Arte de la aventura

La portada `assets/aventura.png` se creó con la herramienta integrada ImageGen para este perfil. Es una escena original de fantasía pixelada con un viajero y tres destinos: taller, torre musical y observatorio. No usa personajes de una franquicia ni fotos personales.

El árbol de habilidades, la ficha de jugador, los logros y la hoguera se dibujan como SVG a partir de datos y geometría; no dependen de generadores externos de tarjetas. Las runas y los brillos son suaves; los números y las etiquetas permanecen fijos. El árbol se muestra en un desplegable para mantener la presentación principal despejada.

## GIF del paisaje

`assets/aventura-viva.gif` añade luciérnagas, estrellas y chispas sobre el paisaje original, que permanece intacto en su PNG. La capa de partículas es geometría propia generada por código; FFmpeg compone y codifica la secuencia de vídeo. El GIF mide 840×280, se muestra a un máximo de 420 px y tiene un bucle de unos 6 segundos. `prefers-reduced-motion` selecciona el PNG estático.

Para regenerarlo: instala Pillow en el entorno de trabajo y coloca FFmpeg en PATH; después ejecuta `python scripts/animar_portada.py`. Los cuadros intermedios quedan en `local/particulas/`, fuera de Git. La acción de estadísticas no necesita Pillow ni FFmpeg.

## Prompt final de la portada

Create one finished ultra-wide 3:1 banner image for a Spanish developer's GitHub profile, ideally 1536 by 512 pixels. This is original premium 16-bit pixel art, like an indie adventure game's title screen. It should feel meticulously art directed and alive, not a generic tech background.

Scene: a tiny hooded adventurer seen from the back with a teal scarf stands at the lower right on an elevated stone path, looking toward three tiny luminous destinations in a lush pixelated nighttime landscape: a workshop with a mechanical pen, a music tower, and a small computer observatory. These represent building practical tools, music, and local AI. Layered indigo mountain silhouettes, deep pine forests, mint fireflies, a few stars, a pale moon, and a very subtle turquoise river. Crisp square pixels, deliberate stepped edges, limited rich palette, no 3D or blur. Night navy #0b1420, forest green #183f3d, jade #4ae3aa, pale mint #d9ffe7, small warm amber lights #ffcc70. The terrain should subtly read as a level-select map. Original artwork only, no recognizable game characters, logos, or franchises.

Composition: wide landscape with a large quiet midnight area in the upper left and center for the title. Place exact large typography on the left in elegantly crafted readable cream pixel letters: "ERICK". Directly below in smaller mint pixel lettering put exactly: "PLAYER 28". Above ERICK, a small spaced uppercase line reads exactly "BUILD / PLAY / REPEAT". Keep all lettering safely inset and perfectly legible. Do not put statistics, skill ratings, badges, UI cards, URLs, additional text, or placeholder labels anywhere. Leave approximately 8 percent safe margin. The landscape stays dense and detailed mostly in the bottom half and right third, with beautiful focused silhouettes and authentic game atmosphere. Finished GitHub profile hero, sophisticated retro pixel-art title screen.
