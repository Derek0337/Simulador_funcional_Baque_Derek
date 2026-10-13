"""Capa lógica: acciones y reglas de combate, separadas de la interfaz.
    Nombre: Baque Hernandez Derek Damian
    Materia: Programación Funcional 5/1
"""

from dataclasses import dataclass, replace
from functools import reduce
from typing import Callable, TypeAlias
from uuid import uuid4

from datos import Dios, EstadoArena


@dataclass(frozen=True)
class AtaqueDivino:
    atacante_id: str
    objetivo_id: str


@dataclass(frozen=True)
class FuriaEspartana:
    atacante_id: str
    objetivo_id: str


@dataclass(frozen=True)
class Curacion:
    objetivo_id: str


@dataclass(frozen=True)
class InvocarDios:
    dios: Dios


Accion: TypeAlias = AtaqueDivino | FuriaEspartana | Curacion | InvocarDios


# Función pura 1/3 y closure; captura factor sin estado global mutable.
def crear_multiplicador_ira(factor: float) -> Callable[[int], int]:
    return lambda danio: max(1, int(danio * factor))


# Pattern matching procesa cada tipo de acción.
# Función pura 2/3; orden superior map recibe transformaciones lambda.
# replace devuelve objetos nuevos sin mutar el estado original.
def procesar_accion(estado: EstadoArena, accion: Accion) -> EstadoArena:
    match accion:
        case AtaqueDivino(atacante_id, objetivo_id) | FuriaEspartana(
            atacante_id, objetivo_id
        ):
            atacante = next(
                filter(lambda dios: dios.id == atacante_id, estado.dioses), None
            )
            objetivo = next(
                filter(lambda dios: dios.id == objetivo_id, estado.dioses), None
            )
            if atacante is None or objetivo is None:
                raise ValueError("Selecciona dioses válidos.")
            if atacante_id == objetivo_id:
                raise ValueError("Un dios no puede atacarse a sí mismo.")
            if atacante.vida <= 0 or objetivo.vida <= 0:
                raise ValueError("Ambos dioses deben seguir en combate.")

            base = max(1, atacante.ataque - objetivo.defensa)
            multiplicador = crear_multiplicador_ira(
                1.5 if isinstance(accion, AtaqueDivino) else 2.5
            )
            danio = min(objetivo.vida, multiplicador(base))
            dioses = tuple(
                map(
                    lambda dios: replace(dios, vida=dios.vida - danio)
                    if dios.id == objetivo_id
                    else dios,
                    estado.dioses,
                )
            )
            nombre_accion = (
                "ataque divino"
                if isinstance(accion, AtaqueDivino)
                else "furia espartana"
            )
            evento = f"{atacante.nombre} usa {nombre_accion}: {danio} de daño a {objetivo.nombre}."

        case Curacion(objetivo_id):
            objetivo = next(
                filter(lambda dios: dios.id == objetivo_id, estado.dioses), None
            )
            if objetivo is None or objetivo.vida <= 0:
                raise ValueError("El objetivo debe estar vivo.")
            vida = min(objetivo.vida_maxima, objetivo.vida + 25)
            recuperado = vida - objetivo.vida
            dioses = tuple(
                map(
                    lambda dios: replace(dios, vida=vida)
                    if dios.id == objetivo_id
                    else dios,
                    estado.dioses,
                )
            )
            evento = f"{objetivo.nombre} recupera {recuperado} puntos de vida."

        case InvocarDios(dios):
            nombre = dios.nombre.strip()
            if not nombre or len(nombre) > 24:
                raise ValueError("El nombre debe tener entre 1 y 24 caracteres.")
            if any(actual.nombre.casefold() == nombre.casefold() for actual in estado.dioses):
                raise ValueError("Ya existe un dios con ese nombre.")
            if len(estado.dioses) >= 12:
                raise ValueError("La arena admite hasta 12 dioses.")
            if not 1 <= dios.vida_maxima <= 500 or not 1 <= dios.ataque <= 100:
                raise ValueError("Vida (1-500) y ataque (1-100) fuera de rango.")
            if not 0 <= dios.defensa <= 10:
                raise ValueError("La defensa debe estar entre 0 y 10.")
            nuevo = replace(dios, nombre=nombre, vida=dios.vida_maxima)
            dioses = estado.dioses + (nuevo,)
            evento = f"{nombre} entra en la arena."

        case _:
            raise TypeError("Tipo de acción no reconocido.")

    return replace(estado, dioses=dioses, registro=(estado.registro + (evento,))[-100:])


# Función pura 3/3; filter y reduce calculan un resumen sin efectos externos.
def resumen_arena(estado: EstadoArena) -> tuple[int, int, int]:
    vivos = tuple(filter(lambda dios: dios.vida > 0, estado.dioses))
    vida_total = reduce(lambda total, vida: total + vida, map(lambda dios: dios.vida, vivos), 0)
    return len(vivos), vida_total, len(estado.dioses)


# Impura 1/2; genera un identificador aleatorio para los nuevos dioses.
def nuevo_id_dios() -> str:
    return str(uuid4())


# Impura 2/2; delega las reglas a la función pura y escribe el evento en consola.
def ejecutar_accion(estado: EstadoArena, accion: Accion) -> EstadoArena:
    nuevo_estado = procesar_accion(estado, accion)
    print(nuevo_estado.registro[-1])
    return nuevo_estado


