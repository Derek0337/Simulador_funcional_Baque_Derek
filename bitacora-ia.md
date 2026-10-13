Bitácora de uso de IA

1. Diseño de la interfaz gráfica y separación de capas

Prompt : Creame una interfaz gráfica con ttkbootstrap tema oscuro para un juego de arena de dioses, separando la lógica en callbacks puros.

Fragmento sugerido por IA: Se generó la estructura de clases de ArenaApp, configuró el grid de Tkinter y añadió los widgets básicos.

Qué se aceptó: El esqueleto visual completo, la disposición en frames y el uso de variables de control como tb.StringVar().

Qué se modificó: Se ajustaron los callbacks de los botones (como _accion) para que únicamente empaqueten los datos visuales y deleguen el trabajo a logica.py, evitando romper la separación de capas obligatoria.

Qué se rechazó / Por qué: Copilot sugirió actualizar la vida de los dioses alterando atributos (ej. dios.vida -= danio) directamente en app.py. Se rechazó tajantemente porque violaba la restricción de inmutabilidad y pureza de la lógica de dominio exigida.

2. Implementación de herramientas funcionales para resúmenes

Prompt: Implementa una función para calcular la cantidad de dioses vivos y su vida total.

Fragmento sugerido por IA: Generó una función imperativa con un contador y un acumulador iterando a través de un clásico bucle for.

Qué se modificó / Por qué: Se adaptó la idea original y se descartó el bucle para construir la función resumen_arena empleando filter (para obtener los dioses vivos) y reduce (para sumar sus puntos de vida). 