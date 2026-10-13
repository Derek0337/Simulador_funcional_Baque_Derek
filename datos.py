"""Capa de estado: modelos y partida inicial de la arena.
    Nombre: Baque Hernandez Derek Damian
    Materia: Programación Funcional 5/1
"""

from dataclasses import dataclass


#Dios es inmutable; cada cambio produce una instancia nueva.
@dataclass(frozen=True)
class Dios:
    id: str
    nombre: str
    vida: int
    vida_maxima: int
    ataque: int
    defensa: int


@dataclass(frozen=True)
class EstadoArena:
    dioses: tuple[Dios, ...]
    registro: tuple[str, ...] = ()


def estado_inicial() -> EstadoArena:
    return EstadoArena(
        dioses=(
            Dios("kratos", "Kratos", 140, 140, 30, 8),
            Dios("atenea", "Atenea", 110, 110, 23, 9),
            Dios("ares", "Ares", 125, 125, 28, 6),
        )
    )
