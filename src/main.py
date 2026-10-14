import ttkbootstrap as tb
from arena.domain.modelo import CiberSamurai, FuerzaCorporativa, EstadoJuego
from arena.entrypoints.gui import AppArena

def crear_estado_inicial() -> EstadoJuego:
    """Construye el estado inmutable inicial del juego."""
    # 1. Creamos al jugador
    jugador = CiberSamurai(
        nombre="Ronin-77",
        integridad=200,
        max_integridad=200,
        energia=10,
        nanobots=3,
        escudos=()  # Tupla vacía para los buffs
    )
    
    # 2. Creamos la colección inmutable de enemigos
    enemigos_totales = (
        FuerzaCorporativa(nombre="Dron de Seguridad", integridad=40, max_integridad=40, ataque=10),
        FuerzaCorporativa(nombre="Ciborg de Asalto", integridad=80, max_integridad=80, ataque=18),
        FuerzaCorporativa(nombre="Mecha Corporativo", integridad=150, max_integridad=150, ataque=30)
    )
    
    # 3. Retornamos el EstadoJuego ensamblado
    return EstadoJuego(
        jugador=jugador,
        enemigo_actual=enemigos_totales[0],    # El primer enemigo entra a la arena
        enemigos=enemigos_totales[1:],         # El resto espera en la tupla
        mensajes=("Sistema de combate iniciado.", "¡Fuerzas corporativas detectadas!")
    )

# Punto de entrada principal de la aplicación
if __name__ == '__main__':
    # Generamos los datos puros
    estado_base = crear_estado_inicial()
    
    # Inicializamos la ventana de ttkbootstrap con un tema "cyberpunk"
    app_root = tb.Window(themename="cyborg") 
    
    # Inyectamos el estado en nuestra Cáscara Imperativa
    app = AppArena(app_root, estado_base)
    
    # Arrancamos el programa
    app_root.mainloop()