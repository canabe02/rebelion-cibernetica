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

        # CONFIGURACIÓN DE COLORES PARA EL HISTORIAL
        self.tree_historial.tag_configure("ataque_jugador", foreground="#00E5FF")  # Cyan
        self.tree_historial.tag_configure("ataque_enemigo", foreground="#FF4444")  # Rojo
        self.tree_historial.tag_configure("buff", foreground="#00FF00")            # Verde
        self.tree_historial.tag_configure("sistema", foreground="#FFD700")         # Dorado
        self.tree_historial.tag_configure("error", foreground="#FFA500")           # Naranja

    def ejecutar_turno(self, accion):

        if not self.estado.corriendo:
            return
            
        if not self.estado.enemigo_actual and len(self.estado.enemigos) == 0:
            return
        nuevo_estado = procesar_accion(self.estado, accion)
        self.estado = nuevo_estado
        self.actualizar_pantalla(self.estado)

    def actualizar_pantalla(self, estado: EstadoJuego):
        j = estado.jugador
        e = estado.enemigo_actual

        self.lbl_nombre_jugador.config(text=j.nombre)
        self.barra_hp_jugador.configure(amountused=j.integridad, amounttotal=j.max_integridad)
        self.lbl_recursos.config(text=f"Energía: {j.energia} | Nanobots: {j.nanobots}")
        text_buffs = ", ".join(map(lambda b: f"Escudo({b.turnos_restantes}T)", j.escudos))
        self.lbl_buffs.config(text=f"Estados Activos: {text_buffs or 'Ninguno'}")

        if e:
            self.lbl_nombre_enemigo.config(text=e.nombre)
            self.barra_hp_enemigo.configure(amountused=e.integridad, amounttotal=e.max_integridad)
            self.lbl_stats_enemigo.config(text=f"Poder de Ataque: {e.ataque}")
        else:
            self.lbl_nombre_enemigo.config(text="Área Despejada")
            self.barra_hp_enemigo.configure(amountused=0, amounttotal=100)
            self.lbl_stats_enemigo.config(text="¡Victoria!")

        for row in self.tree_historial.get_children():
            self.tree_historial.delete(row)
            
        # Parseo visual basado en los Emojis (No toca la lógica)
        for msj in reversed(estado.mensajes[-15:]): 
            tag = "default"
            if "⚔️" in msj or "⚡" in msj: tag = "ataque_jugador"
            elif "⚠️" in msj: tag = "ataque_enemigo"
            elif "💊" in msj or "🛡️" in msj: tag = "buff"
            elif "💥" in msj or "🏆" in msj or "🚨" in msj: tag = "sistema"
            elif "❌" in msj: tag = "error"
            
            self.tree_historial.insert("", "end", values=(msj,), tags=(tag,))