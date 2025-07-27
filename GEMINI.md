# Instrucciones para Gemini

## Descripción del Proyecto
Este es un juego 2D de disparos desarrollado con Pygame. El objetivo es destruir enemigos que caen desde la parte superior de la pantalla.

## Idioma
El idioma principal del código, los comentarios y la comunicación es en español. Mantén la consistencia.

## Dependencias
Para instalar las dependencias, utiliza el archivo `requirements.txt`:
```bash
pip install -r requirements.txt
```

## Cómo Ejecutar el Juego
El punto de entrada de la aplicación es `main.py`. Para ejecutar el juego, usa el siguiente comando:
```bash
python src/main.py
```

## Convenciones de Código
Sigue el estilo de código existente.
Utiliza nombres de variables y funciones en español, como se ve en el código actual (`generacion_enemigos`, `jugador`, etc.).
Asegúrate de que los cambios se integren de forma natural con la estructura del proyecto.
Responde siempre en español, yo también te hablaré en español
Responde con detalle si es técnico, y de forma clara si es general
Evita jerga innecesaria y mantén profesionalidad
Indica si falta información o si el tema no es conocido
Usa elementos existentes en el proyecto #codebase
main.py será el punto de entrada del proyecto
El sistema debe ser modular, íntegro y mantenible
Evita scripts complejos, propón modularizar o refactorizar si es necesario
Usa siempre tabulación para formatear código
Prioriza soluciones simples y seguras
Itera sobre código existente antes de crear desde cero
Evita duplicación de código, reutiliza lógica ya implementada
Solo aplica cambios solicitados o justificados y comprendidos
No introduzcas nuevas tecnologías sin agotar las actuales
En caso de tener que añadir nuevos elementos que sustituyan a los viejos, elimina lo obsoleto para evitar duplicidades
Mantén el código limpio, organizado y documentado
No cambies el código existente sin justificación
Evita cambios de estilo sin justificación
Evita cambios de nombre de variables sin justificación
Evita cambios de nombre de funciones sin justificación
Evita cambios de nombre de clases sin justificación
Evita cambios de nombre de módulos sin justificación
Evita cambios de nombre de archivos sin justificación
Evita cambios de nombre de carpetas sin justificación
Cada función debe tener descripción breve y clara
Todos los scripts deben tener cabecera descriptiva que incluya el nombre del script, autor, fecha y descripción
Verifica que todos los imports (from ...) estén correctamente referenciados
Usa gestión de errores adecuada para asegurar robustez
Registra cambios con fecha, autor y descripción en cada script
Documenta todas las dependencias y mantenlas actualizadas
Usa #codebase en cada mensaje para asegurar acceso completo al proyecto
Mantén una estructura de carpetas clara y coherente
Revisa y refactoriza código regularmente para mejorar calidad y rendimiento
Toda función debe tener un objetivo claro y definido
Sigue una nomenclatura coherente y descriptiva en todo el proyecto
Realiza los cambios necesarios para cumplir con las instrucciones e implementa las mejoras solicitadas
Cuando lancemos comandos por consola para realizar copias o lecturas masivas de ficheros debemos asegurarnos de utilizar las opciones más robustas evitando que los comandos fallen y perder con ello el tiempo. Usar un comando por línea y asegurarse de que el formato y mandatos son correctos.
Adelantate a los errores de replace asegurándote de que el formato y rutas se indican correctamente cuando reemplaces contenido de ficheros. Se muy preciso con el old_string y new_string. Lee bien los ficheros apra asegurarte de que obtienes el contenido exacto y luego constriyes la llamada replace.
Trabajamos en el sistema operativo Windows 11, con Visual Studio Code. Ten esto en cuenta cuando vayas a lanzar comandos por consola para usar los más adecuados para este sistema. Si conoces algún elemento descargable que nos pueda facilitar la tarea, propondrás su descarga y utilización.
Usar rutas absolutas para evitar problemas al empaquetar en exe o con las referencias entre elementos.