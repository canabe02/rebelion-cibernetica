


## Interacción 1: Creación del Modelo de Datos (Fase 1)

- **Prompt usado:** "Actúa como un experto en Python. Genera el código para mi archivo modelo.py. Necesito que implementes las entidades Jugador, Enemigo y el EstadoJuego utilizando @dataclass(frozen=True) para garantizar la inmutabilidad. Además, define al menos tres acciones de combate utilizando Union (Tipos Suma). Regla estricta: Usa tuple en lugar de list para cualquier colección."
- **Código sugerido por IA:**

```python
from dataclasses import dataclass
from typing import Union, Optional

# ==========================================
# TIPOS PRODUCTO (Entidades Inmutables)
# ==========================================

@dataclass(frozen=True)
class Jugador:
    nombre: str
    hp: int
    max_hp: int
    mana: int
    pociones: int

@dataclass(frozen=True)
class Enemigo:
    nombre: str
    hp: int
    max_hp: int
    ataque: int

@dataclass(frozen=True)
class EstadoJuego:
    jugador: Jugador
    enemigos: tuple[Enemigo, ...]  # Se usan tuplas en lugar de listas para garantizar inmutabilidad
    enemigo_actual: Optional[Enemigo]
    mensajes: tuple[str, ...]

# ==========================================
# TIPOS SUMA (Acciones de Combate)
# ==========================================

@dataclass(frozen=True)
class Atacar:
    poder: int

@dataclass(frozen=True)
class Curar:
    cantidad: int

@dataclass(frozen=True)
class UsarObjeto:
    item: str

# El Tipo Suma que agrupa las acciones posibles mutuamente excluyentes
Accion = Union[Atacar, Curar, UsarObjeto]
```

- **Qué se aceptó y justificó:**
  * Acepté la estructura de `@dataclass(frozen=True)` para las entidades principales porque actúan como "Tipos Producto", agrupando variables que deben existir todas a la vez para que el dato tenga sentido. Por ejemplo un jugador tiene vida y mana a la vez.
  * Validé esta implementación porque cumple con el principio de hacer que los estados inválidos sean irrepresentables, ya que el decorador `frozen=True` garantiza que los atributos no puedan ser reasignados y lanzará un `FrozenInstanceError` si algo intenta mutarlos.
  * Acepté el uso de `Union` para modelar las acciones de combate como "Tipos Suma", ya que permite definir opciones que se excluyen mutuamente. Esto es ideal para un menú de acciones, porque el jugador solo puede ejecutar una acción a la vez y esto evita que se generen combinaciones ilógicas.
- **Qué se modificó y justificó:**
  * Me aseguré de restringir a la IA para que no usara arreglos tradicionales para almacenar las agrupaciones de enemigos o escudos.
  * Justifiqué esta restricción porque en Python las estructuras `list` son colecciones mutables que permitirían alterar los datos de forma silenciosa.
  * En su lugar, exigí y validé el uso de `tuple`, ya que es la contraparte inmutable requerida para secuencias que no deben cambiar, protegiendo así al programa de efectos secundarios derivados de estados compartidos


## Interacción 2: Refactorización del Modelo (Temática Rebelión Cibernética)
- **Prompt usado:** "Debo actualizar el código de modelo.py con la nueva temática de Rebelión Cibernética que definimos (Ciber-Samurái, Integridad, Energía, Nanobots). Asegúrate de incluir un atributo para los escudos temporales respetando la inmutabilidad."

- **Código sugerido por IA:**

```python
from dataclasses import dataclass
from typing import Union, Optional

# ==========================================
# TIPOS PRODUCTO (Entidades Inmutables)
# ==========================================

@dataclass(frozen=True)
class EstadoEscudo:
    turnos_restantes: int
    reduccion_dano: int

@dataclass(frozen=True)
class CiberSamurai:
    nombre: str
    integridad: int      # Equivalente a HP
    max_integridad: int
    energia: int         # Equivalente a Maná
    nanobots: int        # Equivalente a Pociones
    escudos: tuple[EstadoEscudo, ...]  # Colección inmutable para los buffs[cite: 6, 13]

@dataclass(frozen=True)
class FuerzaCorporativa:
    nombre: str
    integridad: int
    max_integridad: int
    ataque: int

@dataclass(frozen=True)
class EstadoJuego:
    jugador: CiberSamurai
    enemigos: tuple[FuerzaCorporativa, ...]  # Tupla para garantizar inmutabilidad[cite: 6, 13]
    enemigo_actual: Optional[FuerzaCorporativa]
    mensajes: tuple[str, ...]

# ==========================================
# TIPOS SUMA (Acciones de Combate)
# ==========================================

@dataclass(frozen=True)
class CortePlasma:
    poder_base: int

@dataclass(frozen=True)
class SobrecargaNucleo:
    costo_energia: int

@dataclass(frozen=True)
class ProtocoloEscudo:
    costo_energia: int
    duracion_turnos: int

@dataclass(frozen=True)
class UsarNanobots:
    curacion_base: int

# El Tipo Suma que agrupa las acciones posibles mutuamente excluyentes
Accion = Union[CortePlasma, SobrecargaNucleo, ProtocoloEscudo, UsarNanobots]
```


- **Qué se aceptó y justificó:**
  * Decidí refactorizar el modelo genérico inicial hacia las entidades propias de la lógica de negocio (`CiberSamurai` y `FuerzaCorporativa`) para dotar de originalidad al proyecto. Acepté la refactorización sugerida por la IA porque mantuvo intacta la arquitectura de Tipos Producto (`@dataclass(frozen=True)`) y Tipos Suma (`Union`) definida en el paso anterior.
  * Se validó y aceptó la inclusión del nuevo atributo `escudos: tuple[EstadoEscudo, ...]` dentro de la entidad del jugador para gestionar los estados alterados temporales (*buffs al jugador*).
- **Qué se modificó y justificó:**
  * Durante la revisión de este fragmento, puse especial atención en cómo se almacenaban las colecciones de enemigos y escudos. Según los principios de la Unidad 2, utilizar estructuras como `list` introduce mutabilidad, lo cual es una fuente principal de complejidad y errores debido al estado compartido. Una lista permitiría que los escudos fueran modificados en el sitio (ej. `escudos.append()`), generando efectos secundarios indeseados.
  * Por lo tanto, exigí y justifiqué el uso exclusivo de `tuple`, ya que en Python es la contraparte inmutable estricta para secuencias. 
  * Al hacer esto, garantizo que cuando un escudo expire o se active uno nuevo, el programa no pueda mutar la colección actual, sino que estará obligado a aplicar el patrón de transformación ("Copiar y Actualizar") devolviendo una nueva versión del estado general.


## Interacción 3: Creación de la Capa Lógica (Fase 2)

- **Prompt usado:** "Actúa como un experto en programación funcional en Python. Genera el código para mi archivo logica.py (Fase 2) basándote en las entidades de modelo.py (CiberSamurai, FuerzaCorporativa, EstadoJuego y las acciones de combate). Requisitos estrictos de diseño: Funciones Puras: Implementa la lógica de combate (Corte de Plasma, Sobrecarga de Núcleo, Protocolo de Escudo y Uso de Nanobots) como funciones puras. No uses print ni modifiques variables globales.
Inmutabilidad: Todas las actualizaciones de estado deben hacerse devolviendo una nueva instancia usando la función replace() de dataclasses, sin mutar el estado original en el sitio.
Closure: Crea un closure de validación (por ejemplo, crear_validador_recursos) que encapsule los costos de energía y nanobots en su entorno léxico y retorne una función validadora.
Pattern Matching: Implementa una función central procesar_accion(estado: EstadoJuego, accion: Accion) -> EstadoJuego que utilice match/case para decidir qué habilidad ejecutar según la estructura del dato.
Funciones de Orden Superior (HOF): Incluye una función pura de "fin de turno" que utilice filter para limpiar la tupla de escudos del jugador, eliminando aquellos cuyos turnos_restantes lleguen a cero."

- **Código sugerido por IA:**

```python
from dataclasses import replace
from typing import Callable, Optional
from arena.domain.modelo import (
    CiberSamurai, FuerzaCorporativa, EstadoJuego, EstadoEscudo,
    Accion, CortePlasma, SobrecargaNucleo, ProtocoloEscudo, UsarNanobots
)

TransformadorEstado = Callable[[EstadoJuego], EstadoJuego]

def agregar_mensaje(estado: EstadoJuego, mensaje: str) -> EstadoJuego:
    """Función pura auxiliar para registrar el historial de forma inmutable."""
    return replace(estado, mensajes=estado.mensajes + (mensaje,))

# ==========================================
# REQUISITO 5: Funciones de Orden Superior (HOF)
# ==========================================
def limpiar_escudos_expirados(estado: EstadoJuego) -> EstadoJuego:
    """Reduce los turnos de los escudos y usa `filter` para eliminar los expirados."""
    escudos_actualizados = tuple(
        replace(e, turnos_restantes=e.turnos_restantes - 1) 
        for e in estado.jugador.escudos
    )
    # HOF filter pura sin bucles for mutables
    escudos_vivos = tuple(filter(lambda e: e.turnos_restantes > 0, escudos_actualizados))
    
    jugador_limpio = replace(estado.jugador, escudos=escudos_vivos)
    return replace(estado, jugador=jugador_limpio)

# ==========================================
# REQUISITO 3: Closure Validador
# ==========================================
def crear_validador_recursos(costo_energia: int, costo_nanobots: int, accion_pura: TransformadorEstado) -> TransformadorEstado:
    """
    Closure que captura los costos en su entorno léxico.
    Actúa como guardián antes de delegar a la función pura.
    """
    def ejecutar_con_validacion(estado: EstadoJuego) -> EstadoJuego:
        jugador = estado.jugador
        if jugador.energia < costo_energia:
            return agregar_mensaje(estado, "Fallo: Energía insuficiente para esta habilidad.")
        if jugador.nanobots < costo_nanobots:
            return agregar_mensaje(estado, "Fallo: No te quedan nanobots de curación.")
            
        # Transformación inmutable del pago (Requisito 2)
        jugador_pagado = replace(
            jugador, 
            energia=jugador.energia - costo_energia,
            nanobots=jugador.nanobots - costo_nanobots
        )
        estado_pagado = replace(estado, jugador=jugador_pagado)
        
        return accion_pura(estado_pagado)
    return ejecutar_con_validacion

# ==========================================
# REQUISITO 1 y 2: Funciones Puras e Inmutabilidad
# ==========================================
def aplicar_corte_plasma(poder: int) -> TransformadorEstado:
    def accion(estado: EstadoJuego) -> EstadoJuego:
        if not estado.enemigo_actual: 
            return estado
        enemigo_danado = replace(estado.enemigo_actual, integridad=max(0, estado.enemigo_actual.integridad - poder))
        nuevo_estado = replace(estado, enemigo_actual=enemigo_danado)
        return agregar_mensaje(nuevo_estado, f"Corte de plasma inflige {poder} de daño al sistema enemigo.")
    return accion

def aplicar_uso_nanobots(curacion: int) -> TransformadorEstado:
    def accion(estado: EstadoJuego) -> EstadoJuego:
        j = estado.jugador
        nuevo_hp = min(j.integridad + curacion, j.max_integridad)
        jugador_curado = replace(j, integridad=nuevo_hp)
        nuevo_estado = replace(estado, jugador=jugador_curado)
        return agregar_mensaje(nuevo_estado, f"Sistemas restaurados: +{curacion} de integridad.")
    return accion

def aplicar_protocolo_escudo(duracion: int) -> TransformadorEstado:
    def accion(estado: EstadoJuego) -> EstadoJuego:
        nuevo_escudo = EstadoEscudo(turnos_restantes=duracion, reduccion_dano=5)
        jugador_escudado = replace(estado.jugador, escudos=estado.jugador.escudos + (nuevo_escudo,))
        nuevo_estado = replace(estado, jugador=jugador_escudado)
        return agregar_mensaje(nuevo_estado, f"Protocolo de escudo activado por {duracion} turnos.")
    return accion

def aplicar_sobrecarga(estado: EstadoJuego) -> EstadoJuego:
    if not estado.enemigo_actual: 
        return estado
    enemigo_danado = replace(estado.enemigo_actual, integridad=max(0, estado.enemigo_actual.integridad - 35))
    nuevo_estado = replace(estado, enemigo_actual=enemigo_danado)
    return agregar_mensaje(nuevo_estado, "¡Sobrecarga de núcleo! Daño masivo infligido a la fuerza corporativa.")

# ==========================================
# REQUISITO 4: Pattern Matching Central
# ==========================================
def procesar_accion(estado: EstadoJuego, accion: Accion) -> EstadoJuego:
    """Controlador puro que decide el flujo basándose en la estructura del dato Action."""
    # 1. Aplicamos el efecto de la acción del jugador mediante match/case
    match accion:
        case CortePlasma(poder_base):
            estado_post_jugador = aplicar_corte_plasma(poder_base)(estado)
            
        case UsarNanobots(curacion_base):
            # Costo: 0 energía, 1 nanobot
            validador = crear_validador_recursos(0, 1, aplicar_uso_nanobots(curacion_base))
            estado_post_jugador = validador(estado)
            
        case ProtocoloEscudo(costo_energia, duracion_turnos):
            # Costo: X energía, 0 nanobots
            validador = crear_validador_recursos(costo_energia, 0, aplicar_protocolo_escudo(duracion_turnos))
            estado_post_jugador = validador(estado)
            
        case SobrecargaNucleo(costo_energia):
            validador = crear_validador_recursos(costo_energia, 0, aplicar_sobrecarga)
            estado_post_jugador = validador(estado)
            
        case _:
            estado_post_jugador = estado
            
    # 2. Al final de la acción, ejecutamos la limpieza de escudos (HOF)
    return limpiar_escudos_expirados(estado_post_jugador)
```


- **Qué se aceptó y justificó:**
  * Acepté la implementación generada porque la IA se limitó a traducir y estructurar sintácticamente la arquitectura y las reglas de negocio que ya había diseñado y exigido previamente en el prompt.
  * **Funciones Puras e Inmutabilidad:** Yo ya había determinado que el núcleo matemático del combate debía estar completamente aislado de los efectos secundarios como las impresiones por consola. Validé el código asegurándome de que la IA implementara el patrón de "Copiar y Actualizar" utilizando exclusivamente la función `replace()`. Esto cumple con mi exigencia de inmutabilidad, ya que el estado original nunca se destruye ni se altera en el sitio.
  * **Implementación del Closure:** Previamente analicé la necesidad de un mecanismo para validar los recursos (energía y nanobots) sin repetir código en cada ataque. Dirigí a la IA para que construyera el closure `crear_validador_recursos`, funcionando como un guardián puro antes de ejecutar la acción.
  * **Control de Flujo (Pattern Matching y HOF):** Acepte el enrutador central de los turnos para que se basara en la forma de los datos recibidos. Por ello, exigí el uso de `match/case` para evaluar los Tipos Suma de mis acciones. Además, para la mecánica de limpieza de escudos, ordené explícitamente usar la Función de Orden Superior `filter` con una expresión `lambda`. Acepté el código final porque respetó este diseño declarativo, evitando introducir bucles mutables tradicionales.


## Interacción 4: Creación de la Capa Visual (Fase 3)

- **Prompt usado:** "Actúa como un experto en Python y diseño de interfaces. Genera el código para mi archivo gui.py (Fase 3) utilizando tkinter y ttkbootstrap. La interfaz debe consumir el núcleo funcional de logica.py y las entidades de modelo.py de nuestro proyecto "Rebelión Cibernética".Requisitos estrictos de diseño arquitectónico:Cáscara Imperativa: La clase de la interfaz debe actuar estrictamente como la "cáscara imperativa". Su única responsabilidad será manejar efectos secundarios (dibujar widgets y registrar clics), sin contener absolutamente nada de lógica de combate.   Delegación con Lambdas: Configura los botones de acción (Corte Plasma, Sobrecarga, Escudo, Nanobots) utilizando expresiones lambda en su parámetro command para instanciar los Tipos Suma (Acciones) y enviarlos al núcleo sin ejecutarlos prematuramente.   Actualización Reactiva: Implementa un método impuro actualizar_pantalla(estado: EstadoJuego) que tome el estado inmutable devuelto por la lógica pura y sobrescriba el texto y las barras de progreso (tb.Progressbar o tb.Meter) de la interfaz.   Historial de Batalla: Utiliza un componente de texto o un Treeview para mostrar la tupla inmutable de mensajes del estado, limpiando e insertando los nuevos datos en cada turno. "
- **Código sugerido por IA:**

```python
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from arena.domain.modelo import (
    CiberSamurai, FuerzaCorporativa, EstadoJuego,
    CortePlasma, SobrecargaNucleo, ProtocoloEscudo, UsarNanobots
)
from arena.service_layer.logica import procesar_accion

class AppArena:
    """
    CÁSCARA IMPERATIVA: Esta clase solo maneja efectos secundarios (I/O).
    No contiene ninguna regla de negocio o cálculo de combate.
    """
    def __init__(self, root: tb.Window, estado_inicial: EstadoJuego):
        self.root = root
        self.root.title("Rebelión Cibernética - Arena Funcional")
        self.root.geometry("800x700")
        
        # Estado inmutable actual
        self.estado = estado_inicial
        
        self._construir_ui()
        self.actualizar_pantalla(self.estado)

    def _construir_ui(self):
        # ==========================================
        # SECCIÓN SUPERIOR: EL VISOR (ESTADÍSTICAS)
        # ==========================================
        frame_visor = tb.Frame(self.root, padding=20)
        frame_visor.pack(fill=X)

        # Panel del Jugador (Izquierda)
        panel_jugador = tb.LabelFrame(frame_visor, text=" Ciber-Samurái ", padding=10)
        panel_jugador.pack(side=LEFT, fill=BOTH, expand=True, padx=5)
        
        self.lbl_nombre_jugador = tb.Label(panel_jugador, font=("Helvetica", 14, "bold"))
        self.lbl_nombre_jugador.pack(pady=5)
        
        self.barra_hp_jugador = tb.Meter(
            panel_jugador, metersize=150, padding=5, amounttotal=100,
            metertype="semi", bootstyle="success", subtext="Integridad"
        )
        self.barra_hp_jugador.pack()
        
        self.lbl_recursos = tb.Label(panel_jugador, text="", font=("Helvetica", 11))
        self.lbl_recursos.pack(pady=5)

        self.lbl_buffs = tb.Label(panel_jugador, text="", bootstyle="info")
        self.lbl_buffs.pack(pady=2)

        # Panel del Enemigo (Derecha)
        panel_enemigo = tb.LabelFrame(frame_visor, text=" Fuerza Corporativa ", padding=10)
        panel_enemigo.pack(side=RIGHT, fill=BOTH, expand=True, padx=5)

        self.lbl_nombre_enemigo = tb.Label(panel_enemigo, font=("Helvetica", 14, "bold"))
        self.lbl_nombre_enemigo.pack(pady=5)
        
        self.barra_hp_enemigo = tb.Meter(
            panel_enemigo, metersize=150, padding=5, amounttotal=100,
            metertype="semi", bootstyle="danger", subtext="Integridad"
        )
        self.barra_hp_enemigo.pack()
        
        self.lbl_stats_enemigo = tb.Label(panel_enemigo, text="", font=("Helvetica", 11))
        self.lbl_stats_enemigo.pack(pady=5)

        # ==========================================
        # SECCIÓN CENTRAL: PANEL DE ACCIONES (LAMBDAS)
        # ==========================================
        frame_acciones = tb.LabelFrame(self.root, text=" Comandos del Sistema ", padding=20)
        frame_acciones.pack(fill=X, padx=20, pady=10)

        # Delegación mediante lambdas: Los botones no calculan, solo instancian Tipos Suma
        tb.Button(
            frame_acciones, text="⚔️ Corte de Plasma (0 EN)", bootstyle="primary",
            command=lambda: self.ejecutar_turno(CortePlasma(poder_base=15))
        ).pack(side=LEFT, padx=10, expand=True, fill=X)

        tb.Button(
            frame_acciones, text="⚡ Sobrecarga (3 EN)", bootstyle="danger",
            command=lambda: self.ejecutar_turno(SobrecargaNucleo(costo_energia=3))
        ).pack(side=LEFT, padx=10, expand=True, fill=X)

        tb.Button(
            frame_acciones, text="🛡️ Protocolo Escudo (2 EN)", bootstyle="info",
            command=lambda: self.ejecutar_turno(ProtocoloEscudo(costo_energia=2, duracion_turnos=3))
        ).pack(side=LEFT, padx=10, expand=True, fill=X)

        tb.Button(
            frame_acciones, text="💊 Usar Nanobots (1 NB)", bootstyle="success",
            command=lambda: self.ejecutar_turno(UsarNanobots(curacion_base=30))
        ).pack(side=LEFT, padx=10, expand=True, fill=X)

        # ==========================================
        # SECCIÓN INFERIOR: HISTORIAL DE BATALLA
        # ==========================================
        frame_historial = tb.LabelFrame(self.root, text=" Registro de Combate ", padding=10)
        frame_historial.pack(fill=BOTH, expand=True, padx=20, pady=(0, 20))

        self.tree_historial = tb.Treeview(frame_historial, columns=("mensaje",), show="headings")
        self.tree_historial.heading("mensaje", text="Evento")
        self.tree_historial.pack(fill=BOTH, expand=True)

    def ejecutar_turno(self, accion):
        """Atrapa el evento impuro, llama al núcleo puro y actualiza la pantalla."""
        # Se detiene si el juego terminó
        if not self.estado.enemigo_actual and len(self.estado.enemigos) == 0:
            return

        # Transformación funcional: Recibimos un NUEVO estado inmutable
        nuevo_estado = procesar_accion(self.estado, accion)
        self.estado = nuevo_estado
        
        # Efecto secundario: renderizamos el resultado
        self.actualizar_pantalla(self.estado)

    def actualizar_pantalla(self, estado: EstadoJuego):
        """Muta los widgets de Tkinter para reflejar el estado inmutable recibido."""
        j = estado.jugador
        e = estado.enemigo_actual

        # Actualizar Jugador
        self.lbl_nombre_jugador.config(text=j.nombre)
        self.barra_hp_jugador.configure(amountused=j.integridad, amounttotal=j.max_integridad)
        self.lbl_recursos.config(text=f"Energía: {j.energia} | Nanobots: {j.nanobots}")
        
        # Formatear buffs usando HOF
        text_buffs = ", ".join(map(lambda b: f"Escudo({b.turnos_restantes}T)", j.escudos))
        self.lbl_buffs.config(text=f"Estados Activos: {text_buffs or 'Ninguno'}")

        # Actualizar Enemigo
        if e:
            self.lbl_nombre_enemigo.config(text=e.nombre)
            self.barra_hp_enemigo.configure(amountused=e.integridad, amounttotal=e.max_integridad)
            self.lbl_stats_enemigo.config(text=f"Poder de Ataque: {e.ataque}")
        else:
            self.lbl_nombre_enemigo.config(text="Área Despejada")
            self.barra_hp_enemigo.configure(amountused=0, amounttotal=100)
            self.lbl_stats_enemigo.config(text="¡Victoria!")

        # Actualizar Historial
        for row in self.tree_historial.get_children():
            self.tree_historial.delete(row)
            
        for msj in reversed(estado.mensajes[-15:]):  # Mostrar los últimos 15 mensajes
            self.tree_historial.insert("", "end", values=(msj,))
```


- **Qué se aceptó y justificó:**
  * **Patrón de Cáscara Imperativa:** Desde la fase de diseño de la arquitectura, establecí que la interfaz gráfica debía ser la única zona del programa donde se permitieran efectos secundarios (I/O visual y eventos de usuario). Validé el código generado asegurándome de que la clase `AppArena` actuara estrictamente como una "cáscara" libre de reglas de negocio o cálculos de combate.
  * **Delegación de Eventos con Lambdas:** Para evitar que la interfaz ejecutara lógicas de manera prematura, ordené explícitamente el uso de expresiones `lambda` en los parámetros `command` de los botones. Comprobé que estas funciones anónimas se limitaran a empaquetar la intención del usuario instanciando mis Tipos Suma (las acciones) y las despacharan al núcleo puro, logrando un desacoplamiento perfecto.
  * **Control de la Impureza y Flujo Unidireccional:** Diseñé el flujo para que fuera reactivo. Acepté el método `actualizar_pantalla` sabiendo que mutar los widgets es una impureza inevitable en cualquier UI, pero justifiqué su uso porque está contenida en la frontera del sistema. Este método se limita a leer el `EstadoJuego` inmutable devuelto por mi núcleo y lo proyecta en las barras de progreso y textos.
  * **Historial Reactivo:** Para el registro de combate, exigí el uso de un componente `Treeview`. Supervisé que su actualización se alimentara exclusivamente de la tupla inmutable de mensajes provista por el estado, limpiando y reconstruyendo la vista en cada turno en lugar de almacenar variables de historial mutables dentro de la clase de la interfaz.



## Interacción 5: Refactorización del Ciclo (Contraataque y UI Dinámica)

- **Prompt usado:** "Nos olvidamos de las acciones de los enemigos. Los enemigos deberían ser capaces de aprovechar sus habilidades para atacar en cada turno. Implementemos una logica con el siguiente flujo de acciones: Jugador -> Muerte Enemigo -> Contraataque -> Limpieza
Además, me gustaría que el sistema del historial sea más completo y tenga mejor formato visual (colores)."
- **Código sugerido por IA:**

```python
# Lógica añadida en logica.py:
def resolver_muerte_enemigo(estado: EstadoJuego) -> EstadoJuego:
    e = estado.enemigo_actual
    if e and e.integridad <= 0:
        estado = agregar_mensaje(estado, f"💥 {e.nombre} ha sido destruido.")
        if not estado.enemigos:
            return agregar_mensaje(replace(estado, enemigo_actual=None), "🏆 ¡Victoria! Área despejada.")
        siguiente = estado.enemigos[0]
        return agregar_mensaje(
            replace(estado, enemigo_actual=siguiente, enemigos=estado.enemigos[1:]),
            f"🚨 Nueva amenaza entra a la arena: {siguiente.nombre}."
        )
    return estado

def aplicar_ataque_enemigo(estado: EstadoJuego) -> EstadoJuego:
    e = estado.enemigo_actual
    if not e or e.integridad <= 0 or (estado.mensajes and "❌" in estado.mensajes[-1]):
        return estado
    j = estado.jugador
    reduccion = sum(escudo.reduccion_dano for escudo in j.escudos)
    dano = max(1, e.ataque - reduccion)
    jugador_danado = replace(j, integridad=max(0, j.integridad - dano))
    return agregar_mensaje(replace(estado, jugador=jugador_danado), f"⚠️ {e.nombre} contraataca causando {dano} de daño.")

# Tags añadidos en gui.py:
self.tree_historial.tag_configure("ataque_jugador", foreground="#00E5FF")
self.tree_historial.tag_configure("ataque_enemigo", foreground="#FF4444")
self.tree_historial.tag_configure("buff", foreground="#00FF00")
```

- **Qué se aceptó y justificó:**
  * **Completitud del Pipeline:** Durante las pruebas, identifiqué que el ciclo del turno estaba incompleto, ya que carecía de la respuesta del enemigo. Dirigí a la IA para que construyera las funciones de contraataque y transición de enemigos respetando la pureza matemática. Acepté la solución porque integró estos pasos en la función central `procesar_accion`, transformando el turno en una tubería perfecta (Jugador -> Muerte Enemigo -> Contraataque -> Limpieza).
  * **Inmutabilidad en las Transiciones:** Validé que al eliminar a un enemigo, la transición al siguiente se realizara segmentando la tupla original (ej. `estado.enemigos[1:]`) y utilizando `replace()`. Esto evitó mutar la colección original mediante métodos prohibidos como `.pop()` o `.remove()`.
  * **Separación de Responsabilidades (Colores):** Concebí la necesidad de darle colores al registro de combate para mejorar la experiencia de usuario. Sin embargo, rechacé que el núcleo funcional manejara códigos hexadecimales, ya que eso violaría la separación entre lógica e interfaz. En su lugar, diseñé un sistema donde el núcleo emite mensajes con emojis y validé que la cáscara imperativa (Tkinter) se encargara de mapear visualmente esos caracteres hacia colores (tags), manteniendo el aislamiento arquitectónico.


## Interacción 6: Condición de Derrota y Estados Inválidos (Game Over)

- **Prompt usado:** "Nos olvidamos de algo importante. En caso de que la integridad del jugador llegue a 0 debería pasar la acción de perder y no poder seguir jugando hasta un nuevo intento. Implementemos un atributo inmutable como una bandera booleana que identifique cuando el programa esta corriendo y cuando no"
- **Código sugerido por IA:**

```python
# 1. Agregado en modelo.py:
@dataclass(frozen=True)
class EstadoJuego:
    jugador: CiberSamurai
    enemigos: tuple[FuerzaCorporativa, ...]
    enemigo_actual: Optional[FuerzaCorporativa]
    mensajes: tuple[str, ...]
    corriendo: bool = True  # NUEVO: Bandera inmutable

# 2. Función en logica.py:
def resolver_derrota_jugador(estado: EstadoJuego) -> EstadoJuego:
    if estado.jugador.integridad <= 0:
        return agregar_mensaje(
            replace(estado, corriendo=False),
            "❌ SISTEMA CAÍDO: Tu Ciber-Samurái ha sido destruido. Game Over."
        )
    return estado

# 3. Validación en gui.py (ejecutar_turno):
if not self.estado.corriendo:
    return

```

- **Qué se aceptó y justificó:**
  * **Prevención de Estados Inválidos:** Detecté un error de diseño (edge case) en el modelo: el jugador podía seguir atacando con integridad cero o negativa. Para solucionarlo sin recurrir a bucles mutables (`while` tradicional) ni interrupciones abruptas (`break`/`sys.exit`), decidí incorporar una bandera booleana inmutable (`corriendo: bool = True`) en el `EstadoJuego`.
  * **Evaluación Pura:** Ordené la creación de la función `resolver_derrota_jugador` y la integré como el último paso crítico del pipeline. Validé que esta función simplemente evaluara la integridad y retornara una nueva versión del estado con `corriendo=False` a través de `replace()`.
  * **Bloqueo en la Frontera Impura:** Para hacer efectiva la restricción, establecí una validación temprana (guard clause) en el método `ejecutar_turno` de la interfaz gráfica. Si la bandera indica que el juego terminó, la interfaz bloquea el paso de los clics hacia el núcleo puro. Justifiqué esta decisión porque es la interfaz (la cáscara) la que debe detener la lectura de eventos del usuario, mientras que el núcleo funcional se mantiene ciego y dedicado únicamente a transformar datos si se le solicita.