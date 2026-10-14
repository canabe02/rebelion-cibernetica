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
    integridad: int   
    max_integridad: int
    energia: int         
    nanobots: int       
    escudos: tuple[EstadoEscudo, ...] 

@dataclass(frozen=True)
class FuerzaCorporativa:
    nombre: str
    integridad: int
    max_integridad: int
    ataque: int

@dataclass(frozen=True)
class EstadoJuego:
    jugador: CiberSamurai
    enemigos: tuple[FuerzaCorporativa, ...]  
    enemigo_actual: Optional[FuerzaCorporativa]
    mensajes: tuple[str, ...]
    corriendo: bool = True

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