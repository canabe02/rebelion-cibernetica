from dataclasses import replace
from typing import Callable, Optional
from arena.domain.modelo import (
    CiberSamurai, FuerzaCorporativa, EstadoJuego, EstadoEscudo,
    Accion, CortePlasma, SobrecargaNucleo, ProtocoloEscudo, UsarNanobots
)

# Alias de tipo para funciones de transformación pura: (Estado) -> Estado
TransformadorEstado = Callable[[EstadoJuego], EstadoJuego]


# ==============================================================================
# 1. BASE DE INMUTABILIDAD Y TRANSFORMACIÓN (replace)
# ==============================================================================

def agregar_mensaje(estado: EstadoJuego, mensaje: str) -> EstadoJuego:
    """Función pura auxiliar para registrar eventos sin mutar tuplas."""
    return replace(estado, mensajes=estado.mensajes + (mensaje,))


# ==============================================================================
# 2. FUNCIONES PURAS DE COMBATE (Jugador y Enemigos)
# ==============================================================================

def aplicar_corte_plasma(poder: int) -> TransformadorEstado:
    """Calcula el daño directo al enemigo y retorna una nueva versión del estado."""
    def accion(estado: EstadoJuego) -> EstadoJuego:
        if not estado.enemigo_actual:
            return estado
        enemigo_danado = replace(
            estado.enemigo_actual, 
            integridad=max(0, estado.enemigo_actual.integridad - poder)
        )
        nuevo_estado = replace(estado, enemigo_actual=enemigo_danado)
        return agregar_mensaje(nuevo_estado, f"⚔️ Corte de plasma inflige {poder} de daño al sistema enemigo.")
    return accion

def aplicar_uso_nanobots(curacion: int) -> TransformadorEstado:
    """Restaura la integridad del samurái respetando el tope máximo."""
    def accion(estado: EstadoJuego) -> EstadoJuego:
        j = estado.jugador
        jugador_curado = replace(j, integridad=min(j.integridad + curacion, j.max_integridad))
        return agregar_mensaje(replace(estado, jugador=jugador_curado), f"💊 Sistemas restaurados: +{curacion} de integridad.")
    return accion

def aplicar_protocolo_escudo(duracion: int) -> TransformadorEstado:
    """Agrega un nuevo escudo protector a la tupla inmutable de escudos."""
    def accion(estado: EstadoJuego) -> EstadoJuego:
        nuevo_escudo = EstadoEscudo(turnos_restantes=duracion, reduccion_dano=5)
        jugador_escudado = replace(estado.jugador, escudos=estado.jugador.escudos + (nuevo_escudo,))
        return agregar_mensaje(replace(estado, jugador=jugador_escudado), f"🛡️ Protocolo de escudo activado por {duracion} turnos.")
    return accion

def aplicar_sobrecarga(estado: EstadoJuego) -> EstadoJuego:
    """Ejecuta un ataque crítico de alto impacto."""
    if not estado.enemigo_actual:
        return estado
    enemigo_danado = replace(estado.enemigo_actual, integridad=max(0, estado.enemigo_actual.integridad - 35))
    return agregar_mensaje(replace(estado, enemigo_actual=enemigo_danado), "⚡ ¡Sobrecarga de núcleo! Daño masivo infligido.")

def resolver_muerte_enemigo(estado: EstadoJuego) -> EstadoJuego:
    """Verifica si el enemigo actual cayó y avanza al siguiente usando slicing de tuplas."""
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
    """Aplica el contraataque corporativo mitigado por los escudos activos."""
    e = estado.enemigo_actual
    if not e or e.integridad <= 0 or (estado.mensajes and "❌" in estado.mensajes[-1]):
        return estado
        
    j = estado.jugador
    reduccion = sum(escudo.reduccion_dano for escudo in j.escudos)
    dano = max(1, e.ataque - reduccion)
    
    jugador_danado = replace(j, integridad=max(0, j.integridad - dano))
    return agregar_mensaje(replace(estado, jugador=jugador_danado), f"⚠️ {e.nombre} contraataca causando {dano} de daño.")

def resolver_derrota_jugador(estado: EstadoJuego) -> EstadoJuego:
    """Verifica la caída del jugador y altera la bandera inmutable de ejecución."""
    if estado.jugador.integridad <= 0:
        return agregar_mensaje(
            replace(estado, corriendo=False), 
            "❌ SISTEMA CAÍDO: Tu Ciber-Samurái ha sido destruido. Game Over."
        )
    return estado


# ==============================================================================
# 3. CLOSURE: VALIDADOR DE RECURSOS (Entorno Léxico)
# ==============================================================================

def crear_validador_recursos(costo_energia: int, costo_nanobots: int, accion_pura: TransformadorEstado) -> TransformadorEstado:
    """Closure que retiene los costos en su ámbito léxico para validar antes de ejecutar."""
    def ejecutar_con_validacion(estado: EstadoJuego) -> EstadoJuego:
        jugador = estado.jugador
        if jugador.energia < costo_energia:
            return agregar_mensaje(estado, "❌ Fallo: Energía insuficiente para esta habilidad.")
        if jugador.nanobots < costo_nanobots:
            return agregar_mensaje(estado, "❌ Fallo: No te quedan nanobots de curación.")
            
        jugador_pagado = replace(
            jugador, 
            energia=jugador.energia - costo_energia, 
            nanobots=jugador.nanobots - costo_nanobots
        )
        estado_pagado = replace(estado, jugador=jugador_pagado)
        return accion_pura(estado_pagado)
    return ejecutar_con_validacion


# ==============================================================================
# 4. FUNCIÓN DE ORDEN SUPERIOR (HOF) Y LAMBDA
# ==============================================================================

def limpiar_escudos_expirados(estado: EstadoJuego) -> EstadoJuego:
    """Utiliza la HOF filter y una lambda para descartar escudos vencidos de forma declarativa."""
    escudos_actualizados = tuple(
        replace(e, turnos_restantes=e.turnos_restantes - 1) 
        for e in estado.jugador.escudos
    )
    # HOF 'filter' + lambda de un solo uso para la regla local de permanencia
    escudos_vivos = tuple(filter(lambda e: e.turnos_restantes > 0, escudos_actualizados))
    jugador_limpio = replace(estado.jugador, escudos=escudos_vivos)
    return replace(estado, jugador=jugador_limpio)


# ==============================================================================
# 5. PATTERN MATCHING Y PIPELINE DEL TURNO
# ==============================================================================

def procesar_accion(estado: EstadoJuego, accion: Accion) -> EstadoJuego:
    """Orquesta el turno completo mediante Pattern Matching y composición de transformaciones."""
    # 1. Turno del Jugador (Selección estructural por Tipo Suma)
    match accion:
        case CortePlasma(poder):
            estado_post_jugador = aplicar_corte_plasma(poder)(estado)
        case UsarNanobots(cura):
            estado_post_jugador = crear_validador_recursos(0, 1, aplicar_uso_nanobots(cura))(estado)
        case ProtocoloEscudo(energia, turnos):
            estado_post_jugador = crear_validador_recursos(energia, 0, aplicar_protocolo_escudo(turnos))(estado)
        case SobrecargaNucleo(energia):
            estado_post_jugador = crear_validador_recursos(energia, 0, aplicar_sobrecarga)(estado)
        case _:
            estado_post_jugador = estado
        
    # 2. Pipeline Secuencial del Turno
    estado_post_muerte = resolver_muerte_enemigo(estado_post_jugador)
    estado_post_ataque = aplicar_ataque_enemigo(estado_post_muerte)
    estado_post_derrota = resolver_derrota_jugador(estado_post_ataque)

    # 3. Limpieza final de modificadores
    return limpiar_escudos_expirados(estado_post_derrota)