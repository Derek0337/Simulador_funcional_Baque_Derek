Documento de Análisis: Simulador Arena God of War
1. Problema que resuelve la aplicación

La aplicación resuelve la necesidad de gestionar una arena de combates simulados entre entidades divinas (Dioses) con mecánicas por turnos. El sistema administra de forma segura las estadísticas de hasta 12 personajes (vida, ataque y defensa) y procesa acciones de combate como ataques, curaciones y uso de habilidades especiales, manteniendo un registro cronológico de los eventos sin corromper el estado global de la partida.

2. Estructuras de datos utilizadas

Se utilizaron dataclass con el atributo frozen=True para garantizar la inmutabilidad. Específicamente, se modeló la entidad Dios y el EstadoArena, el cual almacena a los combatientes en una tupla (tuple[Dios, ...]) y el historial en otra tupla de cadenas de texto (tuple[str, ...]). Además, se utilizó un TypeAlias (Accion) para agrupar las clases de datos que representan los eventos del juego (AtaqueDivino, FuriaEspartana, Curacion, InvocarDios).

3. Dónde se aplicó la Unidad 1

Pattern matching (match/case): Se aplicó en la función procesar_accion en logica.py para evaluar el tipo de acción ejecutada y aplicar las reglas correspondientes de forma estructurada.

Funciones de orden superior: Se usaron map y filter en logica.py (por ejemplo, para buscar al atacante/objetivo y para generar la nueva tupla de dioses tras recibir daño o curación).

Modelado de datos: Implementado mediante dataclass inmutables.

Comparación de enfoque (Funcional vs Imperativo): En lugar de usar un bucle imperativo for para buscar y restar la vida de un dios mutando su valor (dios.vida -= danio), se utilizó un enfoque funcional mapeando (map) la colección entera y reemplazando (replace) únicamente al dios afectado para devolver una colección completamente nueva.

4. Dónde se aplicó la Unidad 2

Lambda: Se usaron funciones anónimas lambda dentro de filter y map para condiciones breves (ej. lambda dios: dios.id == atacante_id).

Limitación de Lambda: No conviene usar lambda para validaciones largas, como en la acción InvocarDios, ya que verificar múltiples condiciones (rango de estadísticas, nombres vacíos y duplicados) en una sola línea destruiría la legibilidad y haría imposible lanzar excepciones claras.

Closure, Pureza e Inmutabilidad: Aplicados estrictamente en las reglas de cálculo de daño y en la creación de los nuevos estados de la arena.

Uso de map, filter y reduce: Se implementaron de forma conjunta en la función resumen_arena para filtrar dioses vivos y reducir su vida a una suma total.

5. Qué partes son puras y cuáles impuras

Puras:

crear_multiplicador_ira(factor): Devuelve un closure predecible y sin dependencias externas.

procesar_accion(estado, accion): Recibe un estado, evalúa las reglas y devuelve un estado nuevo sin alterar variables externas.

resumen_arena(estado): Calcula un resumen sin efectos colaterales.

Impuras:

nuevo_id_dios(): Impura por naturaleza al usar uuid4(), el cual genera un valor aleatorio distinto en cada ejecución.

ejecutar_accion(estado, accion): Genera un efecto secundario explícito al imprimir en la consola (print) el último evento registrado.

6. Qué efectos secundarios existen

Existen dos tipos principales de efectos secundarios en el proyecto:

En la Interfaz (Capa Visual): La alteración de la pantalla en app.py, como repintar la lista de dioses activos en los labels de Tkinter, mostrar cuadros de diálogo (Messagebox) y actualizar las listas desplegables (Combobox).

En la consola: La función ejecutar_accion genera un efecto secundario al imprimir texto en la consola de salida estándar (print).

7. Qué parte del estado se manejó de forma inmutable

Todo el estado del dominio se manejó de forma inmutable. Las listas de combatientes y el historial de la batalla se almacenaron en tuplas (que por definición no pueden mutar en Python) y los atributos de los dioses fueron protegidos por dataclass(frozen=True). Las actualizaciones se realizaron exclusivamente con la función replace(), generando siempre una nueva instancia del juego en lugar de modificar la anterior.

8. Qué closure se implementó y para qué

Se implementó el closure crear_multiplicador_ira(factor) en logica.py. Su propósito es capturar y almacenar en su entorno léxico el multiplicador de daño según el tipo de ataque (1.5 para el ataque divino, 2.5 para la furia espartana). Esto permite retornar una función que ya "recuerda" el multiplicador asignado para aplicarlo sobre el daño base, evitando el uso de variables globales.

9. Qué partes sugirió la IA

La IA se utilizó principalmente para la capa visual. Sugirió la estructura de clases de ArenaApp, la configuración del grid de Tkinter y la inclusión de los widgets básicos de ttkbootstrap con el tema oscuro, acelerando el desarrollo de la interfaz.

10. Qué corrigieron o rechazaron de la IA

Se rechazó tajantemente la sugerencia de la IA de actualizar la vida de los dioses alterando atributos de forma directa en los eventos de los botones (ej. dios.vida -= danio dentro de app.py). Se corrigió refactorizando los callbacks visuales para que únicamente capturen los datos y deleguen el procesamiento a la función pura procesar_accion en logica.py, respetando así la separación de capas y la inmutabilidad exigida.

11. Qué aprendieron técnicamente

Se comprendió de manera práctica la importancia de separar estrictamente la interfaz gráfica de la lógica de negocio. Al aplicar principios funcionales como la inmutabilidad y las funciones puras en el manejo del estado (mediante tuplas y replace), se aprendió que es posible desarrollar aplicaciones interactivas predecibles y libres de bugs ocasionados por modificaciones accidentales de memoria compartida.