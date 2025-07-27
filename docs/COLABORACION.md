# Guía de Colaboración

¡Gracias por tu interés en contribuir a este proyecto!

Para asegurar una colaboración fluida y mantener la calidad del código, por favor, sigue estas directrices:

## 1. Estilo de Código
- **Idioma**: Todo el código, comentarios y documentación deben estar en español.
- **Nomenclatura**: Utiliza nombres de variables, funciones y clases descriptivos y en español (ej. `velocidad_jugador`, `calcular_danio`).
- **Indentación**: Usa siempre tabulaciones para la indentación.
- **Comentarios**: Comenta el código cuando sea necesario para explicar la lógica compleja o decisiones de diseño. Evita comentarios obvios.

## 2. Estructura del Proyecto
- **Modularidad**: El proyecto está diseñado para ser modular. Intenta mantener las nuevas funcionalidades encapsuladas y bien separadas.
- **Reutilización**: Antes de escribir nuevo código, verifica si existe alguna función o clase que pueda ser reutilizada.

## 3. Proceso de Contribución
1.  **Clona el repositorio**: `git clone [URL_DEL_REPOSITORIO]`
2.  **Crea una nueva rama**: Para cada nueva característica o corrección de error, crea una rama separada con un nombre descriptivo (ej. `feature/menu-pausa`, `fix/bug-colision`).
3.  **Implementa tus cambios**: Realiza tus modificaciones siguiendo las convenciones de código.
4.  **Prueba tus cambios**: Asegúrate de que tus cambios no introduzcan nuevos errores y que la funcionalidad esperada trabaje correctamente.
5.  **Documenta tus cambios**: Si añades nuevas funciones o modificas significativamente las existentes, actualiza la documentación relevante.
6.  **Realiza un commit claro**: Escribe mensajes de commit descriptivos que expliquen qué cambios has hecho y por qué.
7.  **Envía tus cambios**: `git push origin tu-rama`
8.  **Abre un Pull Request (PR)**: Describe tus cambios en el PR y espera la revisión.

## 4. Consideraciones Adicionales
- **Rutas Absolutas**: Siempre que sea posible, utiliza rutas absolutas para evitar problemas de referencia, especialmente al empaquetar el juego.
- **Gestión de Errores**: Implementa un manejo de errores robusto para asegurar la estabilidad de la aplicación.
- **Actualización de Dependencias**: Si añades nuevas dependencias, asegúrate de incluirlas en `requirements.txt` y de mantener las existentes actualizadas.

¡Gracias por tu colaboración!