# Personalizar el perfil

Este es el repositorio público especial `erickopgaming28/erickopgaming28`: su README se muestra en el perfil. Solo contiene contenido preparado para ser público.

## Mundo y misiones

El README contiene el texto y los enlaces del diario de misiones. El arte original está en `assets/aventura.png`; su origen y prompt se conservan en [ARTE.md](ARTE.md). La fuente Pixelify Sans se incluye con su licencia SIL OFL en `assets/fonts/`.

Las ramas Arcanista, Bardo y Artífice representan los tres proyectos públicos destacados y sus tecnologías. No expresan porcentajes de dominio ni certificaciones.

## Nivel y experiencia

- 100 XP por repositorio público propio, sin forks ni el repositorio del perfil.
- 25 XP por estrella recibida en esos repositorios.
- Nivel = parte entera de XP / 100 + 1.
- La barra muestra el avance de los últimos 100 puntos hasta el siguiente nivel.

El generador consulta exclusivamente el listado público de repositorios y descarta expresamente cualquier entrada privada. Guarda únicamente nombres públicos, idiomas principales, conteos, fecha y fórmula en `assets/progreso.json`. No lee proyectos del disco ni publica actividad privada, tokens, rutas locales o datos de entrenamiento.

Para actualizar, ejecuta **Actions → Actualizar ficha RPG → Run workflow**. También puedes ejecutar `python scripts/actualizar_perfil.py` con Python 3.11 o superior y acceso a internet. En Windows, si no está disponible la base de zonas horarias, instala `tzdata` o usa el entorno Python del estudio que ya la contiene. La acción no tiene programación periódica.

Para regenerar el aspecto sin consultar internet, usa `python scripts/actualizar_perfil.py --desde assets/progreso.json`. Los SVG incluyen las fuentes, dos temas y una versión vertical del árbol para pantallas pequeñas. Las conexiones animadas respetan la preferencia de movimiento reducido.

GitHub controla las zonas externas al README, como avatar, botones, pestañas y contribuciones. Este proyecto personaliza la biografía, la presentación y el contenido del perfil dentro de esas posibilidades.
