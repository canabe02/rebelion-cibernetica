# Análisis Funcional: "Rebelión Cibernética"
# Autor: Carlos Daniel Bernabé Borbor
# Fecha: 13/10/2026
# Curso: Programacion Funcional 5/1


# Análisis Funcional: "Rebelión Cibernética"

## 1. El Problema: Del "Cómo" Imperativo al "Qué" Declarativo
El objetivo principal de esta aplicación es construir un simulador de combates por turnos ambientado en un universo de "Rebelión Cibernética", donde un Ciber-Samurái se enfrenta a diversas Fuerzas Corporativas (drones, ciborgs y mechas) gestionando estratégicamente recursos como energía, nanobots y escudos.

El verdadero desafío arquitectónico fue resolver este simulador abandonando el paradigma imperativo tradicional. En un enfoque imperativo, el diseño se habría centrado en el "cómo": utilizando bucles mutables (`while True`), reasignando variables constantemente y mezclando los cálculos matemáticos con las impresiones en pantalla o la interfaz de usuario. Esto suele generar código acoplado, propenso a errores por estado compartido y difícil de probar.

En su lugar, este proyecto resuelve el problema aplicando un **enfoque funcional declarativo**. El simulador está diseñado como una tubería de transformaciones puras, donde el objetivo es describir "qué" transformación matemática debe aplicarse a los datos en cada turno (por ejemplo, deducir salud o aplicar un escudo), aislando por completo la lógica del negocio de los efectos secundarios de la interfaz gráfica.

## 2. Diseño del Estado y Estructuras de Datos
Para modelar el dominio de la "Rebelión Cibernética", diseñé las estructuras de datos siguiendo los principios de Tipos Algebraicos enseñados en la **Unidad 2**, con el objetivo de hacer que los estados inválidos del juego sean irrepresentables desde el nivel de código:

*   **Tipos Producto:** Utilicé el decorador `@dataclass(frozen=True)` para las entidades base. Esto obliga a que los objetos agrupen todos sus atributos obligatorios al instanciarse (relación "Y"), modelando un estado completo y consistente:
    *   `CiberSamurai`: Agrupa atributos inmutables como `nombre`, `integridad`, `energia`, `nanobots` y una tupla de `escudos`.
    *   `FuerzaCorporativa`: Modela a los enemigos agrupando `nombre`, `integridad`, `max_integridad` y `ataque`.
    *   `EstadoJuego`: Actúa como el contenedor unificado que almacena al jugador, la lista de enemigos restantes, el enemigo actual, un historial de mensajes y una bandera booleana (`corriendo`) para controlar el flujo.
    
*   **Tipos Suma:** Implementé la estructura `Union` para definir un conjunto cerrado de acciones de combate (`CortePlasma`, `SobrecargaNucleo`, `ProtocoloEscudo`, `UsarNanobots`). Esto actúa como una relación "O" mutuamente excluyente, asegurando a nivel de sistema de tipos que el jugador solo puede invocar una estructura válida a la vez, evitando combinaciones ilógicas de habilidades.

*   **Colecciones y Estado Inmutable:** Apliqué estrictamente la inmutabilidad. En Python, las estructuras `list` o `dict` son mutables por defecto, lo que introduce el peligro de alterar referencias compartidas silenciosamente. Por ello, exigí que el historial de mensajes, los buffs (`escudos`) y la secuencia de enemigos se almacenaran usando colecciones `tuple`. Toda modificación en la partida se realiza aplicando el patrón de "Copiar y Actualizar" mediante la función `replace()` de las *dataclasses*, devolviendo siempre un estado de juego nuevo en lugar de destruir el valor original.



## 3. Arquitectura y Gestión de Efectos Secundarios
Una de las lecciones más importantes del curso fue aprender a gestionar el Catálogo de la Impureza. Apliqué el patrón de arquitectura de "Cáscara Imperativa, Núcleo Funcional":

*   **Núcleo Funcional (Partes Puras):** Mi archivo `logica.py` es completamente puro. Contiene funciones matemáticas (como `aplicar_corte_plasma` o `procesar_accion`) que toman un `EstadoJuego`, lo calculan y devuelven un nuevo `EstadoJuego`. No realizan lecturas externas ni modifican el estado global; si reciben los mismos datos, siempre arrojarán el mismo resultado (determinismo).

*   **Cáscara Imperativa (Partes Impuras):** Mi archivo `gui.py` (desarrollado con Tkinter) contiene los efectos secundarios inevitables. Su método `actualizar_pantalla` es inherentemente impuro porque altera un estado externo (la pantalla del usuario, modificando colores y barras de progreso), lo cual clasifica como un efecto secundario de I/O visual. Al aislar esta impureza en la interfaz, protejo la testeabilidad de mi núcleo funcional.

## 4. Herramientas Funcionales y Control de Flujo (Unidad 1)
Para eliminar los bucles y el control de flujo tradicional, implementé herramientas avanzadas del cálculo lambda (**Unidad 1**):

*   **Implementación de un Closure:** Desarrollé la función `crear_validador_recursos`. Este *closure* no es solo una función anidada, sino una "función que recuerda su entorno". Permite atrapar el costo de energía y nanobots en su memoria léxica, actuando como un guardián que deduce los recursos antes de ejecutar la acción pura, evitando ensuciar el código de cada habilidad.

*   **HOFs y Lambdas:** En lugar de usar un bucle `for` para limpiar los escudos que han expirado, utilicé la Función de Orden Superior `filter` acompañada de una función anónima `lambda`. Esto me permitió expresar declarativamente la regla de conservación ("mantener solo si turnos > 0") en una sola línea. También utilicé `lambda` en mi interfaz gráfica para retrasar la evaluación de los eventos de los botones.

*   **Pattern Matching:** Para controlar el turno, evité las cadenas imperativas de `if/isinstance` y utilicé el moderno `match/case` de Python. Al hacer *pattern matching* sobre mi Tipo Suma (la acción), la estructura misma del dato es la que decide el camino de la ejecución de forma limpia y declarativa.

## 5. Colaboración con Inteligencia Artificial y Aprendizajes
El desarrollo de esta práctica se realizó en modalidad de co-pilotaje con Gemini, asumiendo yo el rol de Arquitecto de Software:

*   **Qué sugirió la IA:** La IA fue fundamental para redactar rápidamente el código repetitivo de las clases de datos (`@dataclass`) y para empaquetar la lógica visual del visor y los botones usando `ttkbootstrap`.

*   **Qué se corrigió y rechazó:** Como director del código, rechacé las sugerencias de la IA cuando intentaba optimizar usando arreglos (`list`) para almacenar mis listas de enemigos, obligándola a refactorizar usando `tuple` para asegurar la inmutabilidad. Además, identifiqué un "edge case" arquitectónico: la IA no había estructurado el ataque del enemigo ni la condición de derrota. Le exigí rediseñar el control de flujo integrando estos eventos como pasos puros del *pipeline* mediante la bandera `corriendo=False`, bloqueando clics en la cáscara impura sin alterar la lógica matemática.

*   **Aprendizaje Técnico:** Comprendí que el paradigma funcional no trata de hacer menos código, sino de hacerlo más predecible. Aprendí a identificar cómo la mutación (cambiar variables en el sitio) puede causar efectos secundarios difíciles de rastrear, y cómo separar las responsabilidades del sistema entre un cálculo matemático determinista (el núcleo) y la interacción con el usuario (la cáscara impura) eleva drásticamente la calidad y mantenibilidad del software.