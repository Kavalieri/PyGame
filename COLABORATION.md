# Directrices de Colaboración para PyGame

Este documento detalla las directrices y convenciones a seguir para todos los colaboradores del proyecto PyGame. El objetivo es mantener la consistencia, la calidad del código y facilitar el trabajo en equipo.

## Idioma
Todo el código, comentarios, documentación y comunicación dentro del proyecto debe realizarse en **español**.

## Convenciones de Código

### Estilo y Formato
*   **Indentación**: Utiliza siempre **tabulaciones** para la indentación del código.
*   **Nomenclatura**: Sigue la nomenclatura existente en el proyecto. Utiliza nombres de variables, funciones, clases y módulos en español, descriptivos y coherentes (ej. `generacion_enemigos`, `jugador`, `calcular_puntuacion`).
*   **Consistencia**: Mimica el estilo, la estructura, las elecciones de framework y los patrones arquitectónicos del código existente.

### Modularidad y Reutilización
*   **Modularidad**: El sistema debe ser modular, íntegro y mantenible. Si una función o script se vuelve demasiado complejo, propón modularizarlo o refactorizarlo.
*   **Reutilización**: Prioriza la reutilización de lógica ya implementada. Evita la duplicación de código.
*   **Objetivo de Funciones**: Cada función debe tener un objetivo claro y definido.

### Documentación
*   **Comentarios**: Añade comentarios de código de forma concisa. Enfócate en *por qué* se hace algo, especialmente para lógica compleja, más que en *qué* se hace.
*   **Cabeceras de Archivo**: Todos los scripts deben tener una cabecera descriptiva que incluya el nombre del script, autor, fecha y una breve descripción de su propósito.
*   **Documentación de Funciones**: Cada función debe tener una descripción breve y clara de su propósito, sus parámetros y lo que retorna.

### Gestión de Cambios
*   **Cambios Justificados**: Solo aplica cambios solicitados o justificados y comprendidos. No introduzcas nuevas tecnologías sin agotar las actuales.
*   **Evitar Cambios Innecesarios**: Evita cambios de estilo, nombre de variables, funciones, clases, módulos o archivos sin una justificación clara y consensuada.
*   **Eliminación de Obsoleto**: Si se añaden nuevos elementos que sustituyen a los viejos, elimina lo obsoleto para evitar duplicidades.
*   **Revisión y Refactorización**: Revisa y refactoriza el código regularmente para mejorar la calidad y el rendimiento.

### Robustez y Mantenimiento
*   **Gestión de Errores**: Implementa una gestión de errores adecuada para asegurar la robustez del sistema.
*   **Dependencias**: Documenta todas las dependencias en `requirements.txt` y mantenlas actualizadas.
*   **Imports**: Verifica que todos los imports (`from ...`) estén correctamente referenciados.

## Estructura del Proyecto
*   **Carpetas**: Mantén una estructura de carpetas clara y coherente.
*   **Punto de Entrada**: `main.py` será el punto de entrada principal del proyecto.

## Proceso de Desarrollo
*   **Iteración**: Itera sobre el código existente antes de crear desde cero.
*   **Soluciones Simples**: Prioriza soluciones simples y seguras.
*   **Verificación**: Antes de finalizar una tarea, asegúrate de que los cambios se integren de forma natural con la estructura del proyecto y que no introduzcan nuevos errores.

Al seguir estas directrices, aseguramos un entorno de desarrollo colaborativo y eficiente para el proyecto PyGame.