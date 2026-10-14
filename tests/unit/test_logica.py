import pytest
from arena.domain.modelo import (
    CiberSamurai, FuerzaCorporativa, EstadoJuego, EstadoEscudo,
    CortePlasma, UsarNanobots, ProtocoloEscudo
)
from arena.service_layer.logica import (
    procesar_accion, limpiar_escudos_expirados, resolver_derrota_jugador
)

@pytest.fixture
def estado_inicial():
    """Fixture que provee un estado base limpio e inmutable para cada prueba."""
    jugador = CiberSamurai(
        nombre="Ciber-Samurái",
        integridad=100,
        max_integridad=100,
        energia=30,
        nanobots=2,
        escudos=()
    )
    enemigo = FuerzaCorporativa(
        nombre="Dron de Asalto",
        integridad=50,
        max_integridad=50,
        ataque=10
    )
    return EstadoJuego(
        jugador=jugador,
        enemigos=(),
        enemigo_actual=enemigo,
        mensajes=("Inicio de prueba",),
        corriendo=True
    )

# -------------------------------------------------------------
# 1. Prueba de Función Pura y Transición de Daño
# -------------------------------------------------------------
def test_corte_plasma_reduce_integridad_enemigo(estado_inicial):
    # Ejecutamos la acción pura
    nuevo_estado = procesar_accion(estado_inicial, CortePlasma(poder_base=15))
    
    # Verificamos que el enemigo recibió el daño
    assert nuevo_estado.enemigo_actual.integridad == 35
    # Verificamos que el estado original NO fue mutado (Inmutabilidad)
    assert estado_inicial.enemigo_actual.integridad == 50

# -------------------------------------------------------------
# 2. Prueba del Closure (Validación de Recursos)
# -------------------------------------------------------------
def test_nanobots_fallan_si_no_hay_recursos(estado_inicial):
    # Creamos un jugador sin nanobots
    jugador_sin_bots = estado_inicial.jugador.__class__(
        nombre="Samurái", integridad=50, max_integridad=100, energia=30, nanobots=0, escudos=()
    )
    estado_sin_recursos = estado_inicial.__class__(
        jugador=jugador_sin_bots,
        enemigos=(),
        enemigo_actual=estado_inicial.enemigo_actual,
        mensajes=(),
        corriendo=True
    )

    # Intentamos curar: el closure debe bloquear el consumo
    nuevo_estado = procesar_accion(estado_sin_recursos, UsarNanobots(curacion_base=25))
    
    assert nuevo_estado.jugador.integridad == 50  # No se curó
    assert any("❌" in m for m in nuevo_estado.mensajes)  # Emitió mensaje de fallo

# -------------------------------------------------------------
# 3. Prueba de la HOF (Filtrado de Escudos Expirados)
# -------------------------------------------------------------
def test_limpiar_escudos_expirados_filtra_correctamente(estado_inicial):
    escudo_por_vencer = EstadoEscudo(turnos_restantes=1, reduccion_dano=5)
    escudo_activo = EstadoEscudo(turnos_restantes=3, reduccion_dano=5)
    
    jugador_con_escudos = estado_inicial.jugador.__class__(
        nombre="Samurái", integridad=100, max_integridad=100, energia=30, nanobots=2,
        escudos=(escudo_por_vencer, escudo_activo)
    )
    estado = estado_inicial.__class__(
        jugador=jugador_con_escudos, enemigos=(), enemigo_actual=None, mensajes=(), corriendo=True
    )

    # Ejecutamos la HOF
    estado_limpio = limpiar_escudos_expirados(estado)
    
    # El de 1 turno debió reducirse a 0 y ser eliminado por filter()
    assert len(estado_limpio.jugador.escudos) == 1
    assert estado_limpio.jugador.escudos[0].turnos_restantes == 2

# -------------------------------------------------------------
# 4. Prueba de la Condición de Derrota (Game Over Inmutable)
# -------------------------------------------------------------
def test_resolver_derrota_cambia_bandera_corriendo(estado_inicial):
    jugador_caido = estado_inicial.jugador.__class__(
        nombre="Samurái", integridad=0, max_integridad=100, energia=0, nanobots=0, escudos=()
    )
    estado_derrota = estado_inicial.__class__(
        jugador=jugador_caido, enemigos=(), enemigo_actual=None, mensajes=(), corriendo=True
    )

    resultado = resolver_derrota_jugador(estado_derrota)
    
    assert resultado.corriendo is False
    assert any("SISTEMA CAÍDO" in m for m in resultado.mensajes)