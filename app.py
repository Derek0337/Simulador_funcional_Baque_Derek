"""Capa visual: interfaz ttkbootstrap de la arena inspirada en God of War.
    Nombre: Baque Hernandez Derek Damian
    Materia: Programación Funcional 5/1
"""

import ttkbootstrap as tb
from ttkbootstrap.dialogs import Messagebox

from datos import Dios, EstadoArena, estado_inicial
from logica import (
    AtaqueDivino,
    Curacion,
    FuriaEspartana,
    InvocarDios,
    ejecutar_accion,
    nuevo_id_dios,
    resumen_arena,
)


class ArenaApp(tb.Window):
    def __init__(self) -> None:
        #  tema oscuro ttkbootstrap para la temática God of War.
        super().__init__(themename="superhero")
        self.title("God of War | Arena de los dioses")
        self.geometry("900x600")
        self.minsize(780, 520)
        self.estado: EstadoArena = estado_inicial()

        self.nombre = tb.StringVar()
        self.vida = tb.StringVar(value="100")
        self.ataque = tb.StringVar(value="20")
        self.defensa = tb.StringVar(value="5")
        self.atacante = tb.StringVar()
        self.objetivo = tb.StringVar()

        self._crear_interfaz()
        self._actualizar()

    def _crear_interfaz(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        cabecera = tb.Frame(self, padding=20)
        cabecera.grid(row=0, column=0, sticky="ew")
        tb.Label(
            cabecera,
            text="GOD OF WAR  |  ARENA DE LOS DIOSES",
            font=("Segoe UI", 20, "bold"),
            bootstyle="danger",
        ).grid(row=0, column=0, sticky="w")
        tb.Label(
            cabecera,
            text="Dioses se enfrentan por el Olimpo",
            bootstyle="secondary",
        ).grid(row=1, column=0, sticky="w", pady=(4, 0))

        cuerpo = tb.Frame(self, padding=(20, 0, 20, 20))
        cuerpo.grid(row=1, column=0, sticky="nsew")
        cuerpo.columnconfigure(0, weight=1)
        cuerpo.columnconfigure(1, weight=2)
        cuerpo.rowconfigure(0, weight=1)

        izquierda = tb.Frame(cuerpo)
        izquierda.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        izquierda.columnconfigure(0, weight=1)
        izquierda.rowconfigure(0, weight=1)

        roster = tb.Labelframe(
            izquierda, text="Dioses de la arena", padding=12, bootstyle="danger"
        )
        roster.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        roster.columnconfigure(0, weight=1)
        self.lista_dioses = tb.Frame(roster)
        self.lista_dioses.grid(row=0, column=0, sticky="new")

        alta = tb.Labelframe(
            izquierda, text="Invocar personaje", padding=12, bootstyle="secondary"
        )
        alta.grid(row=1, column=0, sticky="ew")
        alta.columnconfigure(1, weight=1)
        for fila, (texto, variable) in enumerate(
            (
                ("Nombre", self.nombre),
                ("Vida", self.vida),
                ("Ataque", self.ataque),
                ("Defensa (0–10)", self.defensa),
            )
        ):
            tb.Label(alta, text=texto).grid(row=fila, column=0, sticky="w", pady=3)
            tb.Entry(alta, textvariable=variable).grid(
                row=fila, column=1, sticky="ew", padx=(8, 0), pady=3
            )
        tb.Button(
            alta,
            text="Invocar",
            bootstyle="success",
            command=lambda: self._invocar(),
        ).grid(row=4, column=0, columnspan=2, sticky="ew", pady=(8, 0))

        derecha = tb.Frame(cuerpo)
        derecha.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        derecha.columnconfigure(0, weight=1)
        derecha.rowconfigure(2, weight=1)

        info = tb.Labelframe(
            derecha, text="Estado de la batalla", padding=12, bootstyle="info"
        )
        info.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.resumen = tb.Label(info, text="", font=("Segoe UI", 11, "bold"))
        self.resumen.grid(row=0, column=0, sticky="w")

        acciones = tb.Labelframe(
            derecha, text="Acciones divinas", padding=12, bootstyle="primary"
        )
        acciones.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        acciones.columnconfigure(1, weight=1)
        tb.Label(acciones, text="Dios activo").grid(row=0, column=0, sticky="w", pady=3)
        self.selector_atacante = tb.Combobox(
            acciones, textvariable=self.atacante, state="readonly"
        )
        self.selector_atacante.grid(row=0, column=1, sticky="ew", pady=3)
        tb.Label(acciones, text="Objetivo").grid(row=1, column=0, sticky="w", pady=3)
        self.selector_objetivo = tb.Combobox(
            acciones, textvariable=self.objetivo, state="readonly"
        )
        self.selector_objetivo.grid(row=1, column=1, sticky="ew", pady=3)

        botones = tb.Frame(acciones)
        botones.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(8, 0))
        for columna in range(3):
            botones.columnconfigure(columna, weight=1)
        # REQUISITO: bootstyle semántico para comunicar el efecto de cada acción.
        for columna, (texto, tipo, estilo) in enumerate(
            (
                ("Ataque divino", "ataque", "danger"),
                ("Furia espartana", "furia", "warning"),
                ("Curación", "curacion", "success"),
            )
        ):
            tb.Button(
                botones,
                text=texto,
                bootstyle=estilo,
                command=lambda accion=tipo: self._accion(accion),
            ).grid(row=0, column=columna, sticky="ew", padx=4)

        panel_registro = tb.Labelframe(
            derecha, text="Crónica de combate", padding=10, bootstyle="secondary"
        )
        panel_registro.grid(row=2, column=0, sticky="nsew")
        panel_registro.columnconfigure(0, weight=1)
        panel_registro.rowconfigure(0, weight=1)
        self.registro = tb.Text(
            panel_registro, height=8, wrap="word", state="disabled"
        )
        self.registro.grid(row=0, column=0, sticky="nsew")

    def _invocar(self) -> None:
        
        try:
            dios = Dios(
                nuevo_id_dios(),
                self.nombre.get(),
                0,
                int(self.vida.get()),
                int(self.ataque.get()),
                int(self.defensa.get()),
            )
            self.estado = ejecutar_accion(self.estado, InvocarDios(dios))
        except ValueError as error:
            Messagebox.show_error(str(error), "No se pudo invocar")
            return
        self.nombre.set("")
        self._actualizar()

    def _accion(self, tipo: str) -> None:
        """Traduce la selección visual en una acción y la pasa a logica.py."""
        # los callbacks solo preparan la acción; reglas y cambios van a logica.py.
        seleccion = self.selector_atacante.get()
        objetivo = self.selector_objetivo.get()
        atacante_id = next(
            (dios.id for dios in self.estado.dioses if dios.nombre == seleccion), ""
        )
        objetivo_id = next(
            (dios.id for dios in self.estado.dioses if dios.nombre == objetivo), ""
        )
        if tipo == "ataque":
            accion = AtaqueDivino(atacante_id, objetivo_id)
        elif tipo == "furia":
            accion = FuriaEspartana(atacante_id, objetivo_id)
        else:
            accion = Curacion(objetivo_id)

        try:
            self.estado = ejecutar_accion(self.estado, accion)
        except ValueError as error:
            Messagebox.show_error(str(error), "Acción no disponible")
            return
        self._actualizar()

    def _actualizar(self) -> None:
        """Representa el estado actual en los widgets."""
        for widget in self.lista_dioses.winfo_children():
            widget.destroy()

        for fila, dios in enumerate(self.estado.dioses):
            estado = "CAÍDO" if dios.vida <= 0 else "EN COMBATE"
            estilo = "danger" if dios.vida <= 0 else "success"
            tb.Label(
                self.lista_dioses,
                text=f"{dios.nombre}  ·  {estado}",
                bootstyle=estilo,
                font=("Segoe UI", 11, "bold"),
            ).grid(row=fila * 2, column=0, sticky="w", pady=(5, 0))
            tb.Label(
                self.lista_dioses,
                text=f"Vida {dios.vida}/{dios.vida_maxima}   ATQ {dios.ataque}   DEF {dios.defensa}",
                bootstyle="secondary",
            ).grid(row=fila * 2 + 1, column=0, sticky="w", pady=(0, 4))

        nombres = tuple(dios.nombre for dios in self.estado.dioses)
        self.selector_atacante.configure(values=nombres)
        self.selector_objetivo.configure(values=nombres)
        if nombres:
            if self.atacante.get() not in nombres:
                self.atacante.set(nombres[0])
            if self.objetivo.get() not in nombres:
                self.objetivo.set(nombres[1] if len(nombres) > 1 else nombres[0])

        vivos, vida_total, total = resumen_arena(self.estado)
        self.resumen.configure(text=f"Dioses en pie: {vivos}/{total}  ·  Vida total: {vida_total}")
        self.registro.configure(state="normal")
        self.registro.delete("1.0", "end")
        self.registro.insert("end", "\n".join(reversed(self.estado.registro)))
        self.registro.configure(state="disabled")
        self.registro.see("1.0")


if __name__ == "__main__":
    ArenaApp().mainloop()
