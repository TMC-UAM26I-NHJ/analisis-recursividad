from __future__ import annotations

from typing import Any


Nodo = dict[str, Any]


def crear_nodo(etiqueta: str) -> Nodo:
    """
    Crea un nodo del árbol de llamadas.

    Cada nodo se representa con un diccionario que contiene:
    - 'etiqueta': texto descriptivo de la llamada actual.
    - 'hijos': lista con los nodos hijos generados por llamadas recursivas.

    Args:
        etiqueta: Texto que identifica la llamada actual.

    Returns:
        Un diccionario que representa un nodo del árbol.
    """
    return {
        "etiqueta": etiqueta,
        "hijos": []
    }


def imprimir_arbol(nodo: Nodo, prefijo: str = "", es_ultimo: bool = True) -> None:
    """
    Imprime un árbol con formato jerárquico.

    La función imprime primero el nodo actual y después recorre
    recursivamente cada uno de sus hijos.

    Args:
        nodo: Nodo actual que se desea imprimir.
        prefijo: Cadena auxiliar para conservar la forma visual del árbol.
        es_ultimo: Indica si el nodo actual es el último hijo de su nivel.

    Returns:
        None.
    """
    if es_ultimo:
        conector = "└── "
        nuevo_prefijo = prefijo + "    "
    else:
        conector = "├── "
        nuevo_prefijo = prefijo + "│   "

    print(prefijo + conector + nodo["etiqueta"])

    cantidad_hijos = len(nodo["hijos"])

    for indice, hijo in enumerate(nodo["hijos"]):
        hijo_es_ultimo = indice == cantidad_hijos - 1
        imprimir_arbol(hijo, nuevo_prefijo, hijo_es_ultimo)


def fibonacci_recursivo(n: int) -> tuple[int, Nodo, int]:
    """
    Calcula Fibonacci de forma recursiva y construye el árbol de llamadas.

    La función regresa tres valores:
    1. El resultado numérico de fib(n).
    2. El nodo raíz del subárbol correspondiente a la llamada actual.
    3. El total de llamadas realizadas dentro de este subproblema.

    Args:
        n: Valor de entrada para Fibonacci.

    Returns:
        Una tupla con:
        - resultado de Fibonacci
        - nodo raíz del árbol de llamadas
        - total de llamadas realizadas
    """
    nodo_actual = crear_nodo(f"fib({n})")

    if n <= 1:
        resultado = n
        total_llamadas = 1
        return resultado, nodo_actual, total_llamadas

    resultado_izquierdo, hijo_izquierdo, llamadas_izquierdas = fibonacci_recursivo(n - 1)
    resultado_derecho, hijo_derecho, llamadas_derechas = fibonacci_recursivo(n - 2)

    nodo_actual["hijos"].append(hijo_izquierdo)
    nodo_actual["hijos"].append(hijo_derecho)

    resultado = resultado_izquierdo + resultado_derecho
    total_llamadas = 1 + llamadas_izquierdas + llamadas_derechas

    return resultado, nodo_actual, total_llamadas


def fibonacci_recursivo_memoria(
    n: int,
    memo: dict[int, int] | None = None
) -> tuple[int, Nodo, int]:
    """
    Calcula Fibonacci con memoria dinámica y construye el árbol de llamadas.

    Si un valor ya fue calculado, no se vuelve a expandir su subárbol.
    En ese caso, el nodo se marca con la leyenda '[memo=valor]'.

    Args:
        n: Valor de entrada para Fibonacci.
        memo: Diccionario que almacena resultados ya calculados.

    Returns:
        Una tupla con:
        - resultado de Fibonacci
        - nodo raíz del árbol de llamadas
        - total de llamadas realizadas
    """
    if memo is None:
        memo = {}

    if n in memo:
        nodo_actual = crear_nodo(f"fib({n}) [memo={memo[n]}]")
        resultado = memo[n]
        total_llamadas = 1
        return resultado, nodo_actual, total_llamadas

    nodo_actual = crear_nodo(f"fib({n})")

    if n <= 1:
        memo[n] = n
        resultado = n
        total_llamadas = 1
        return resultado, nodo_actual, total_llamadas

    resultado_izquierdo, hijo_izquierdo, llamadas_izquierdas = fibonacci_recursivo_memoria(
        n - 1,
        memo
    )
    resultado_derecho, hijo_derecho, llamadas_derechas = fibonacci_recursivo_memoria(
        n - 2,
        memo
    )

    nodo_actual["hijos"].append(hijo_izquierdo)
    nodo_actual["hijos"].append(hijo_derecho)

    resultado = resultado_izquierdo + resultado_derecho
    memo[n] = resultado
    total_llamadas = 1 + llamadas_izquierdas + llamadas_derechas

    return resultado, nodo_actual, total_llamadas


def busqueda_binaria_arbol(
    arreglo: list[int],
    objetivo: int,
    izquierda: int,
    derecha: int
) -> tuple[int, Nodo, int]:
    """
    Realiza búsqueda binaria recursiva y construye el árbol de llamadas.

    Cada llamada genera un nodo con el segmento actual del arreglo que
    está siendo analizado.

    Args:
        arreglo: Lista ordenada en la que se desea buscar.
        objetivo: Valor que se desea encontrar.
        izquierda: Índice izquierdo del rango de búsqueda actual.
        derecha: Índice derecho del rango de búsqueda actual.

    Returns:
        Una tupla con:
        - índice encontrado, o -1 si no existe
        - nodo raíz del árbol de llamadas
        - total de llamadas realizadas
    """
    segmento_actual = arreglo[izquierda:derecha + 1]
    etiqueta = "buscar(" + str(segmento_actual) + ")"
    nodo_actual = crear_nodo(etiqueta)

    total_llamadas = 1

    if izquierda > derecha:
        nodo_actual["etiqueta"] += " -> no encontrado"
        return -1, nodo_actual, total_llamadas

    medio = (izquierda + derecha) // 2

    if arreglo[medio] == objetivo:
        nodo_actual["etiqueta"] += " -> encontrado en indice " + str(medio)
        return medio, nodo_actual, total_llamadas

    if objetivo < arreglo[medio]:
        resultado, hijo, llamadas = busqueda_binaria_arbol(
            arreglo,
            objetivo,
            izquierda,
            medio - 1
        )
        nodo_actual["hijos"].append(hijo)
        total_llamadas = total_llamadas + llamadas
        return resultado, nodo_actual, total_llamadas

    resultado, hijo, llamadas = busqueda_binaria_arbol(
        arreglo,
        objetivo,
        medio + 1,
        derecha
    )
    nodo_actual["hijos"].append(hijo)
    total_llamadas = total_llamadas + llamadas

    return resultado, nodo_actual, total_llamadas


def ejecutar_fibonacci(n: int) -> None:
    """
    Ejecuta y muestra dos versiones de Fibonacci:
    - recursiva simple
    - recursiva con memoria dinámica

    Args:
        n: Valor que se utilizará en la demostración.

    Returns:
        None.
    """
    print("=" * 70)
    print("FIBONACCI SIN MEMORIA DINAMICA")
    print("=" * 70)

    resultado, raiz, total_llamadas = fibonacci_recursivo(n)

    print("\nArbol de llamadas:")
    imprimir_arbol(raiz)

    print("\nResumen:")
    print(f"Resultado: {resultado}")
    print(f"Total de llamadas: {total_llamadas}")

    print("\n" + "=" * 70)
    print("FIBONACCI CON MEMORIA DINAMICA")
    print("=" * 70)

    resultado_memo, raiz_memo, total_llamadas_memo = fibonacci_recursivo_memoria(n)

    print("\nArbol de llamadas:")
    imprimir_arbol(raiz_memo)

    print("\nResumen:")
    print(f"Resultado: {resultado_memo}")
    print(f"Total de llamadas: {total_llamadas_memo}")


def ejecutar_busqueda(arreglo: list[int], objetivo: int) -> None:
    """
    Ejecuta la búsqueda binaria recursiva y muestra su árbol de llamadas.

    Args:
        arreglo: Lista ordenada en la que se realizará la búsqueda.
        objetivo: Valor que se desea localizar.

    Returns:
        None.
    """
    print("=" * 70)
    print("BUSQUEDA BINARIA")
    print("=" * 70)

    resultado, raiz, total_llamadas = busqueda_binaria_arbol(
        arreglo,
        objetivo,
        0,
        len(arreglo) - 1
    )

    print("\nArbol de llamadas:")
    imprimir_arbol(raiz)

    print("\nResumen:")
    print(f"Indice encontrado: {resultado}")
    print(f"Total de llamadas: {total_llamadas}")


if __name__ == "__main__":
    ejecutar_fibonacci(6)

    print("\n" + "#" * 70 + "\n")

    arreglo_prueba = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    objetivo_prueba = 6
    ejecutar_busqueda(arreglo_prueba, objetivo_prueba)
    
    valores_n:list[int] =[]
    llamadas_sin_memoria: list[int] = []
    llamadas_con_memoria: list[int] = []

    for i in range(0, 30, 1):
        _, _, ejecucionsin = fibonacci_recursivo(i)
        _,_,ejecucion = fibonacci_recursivo_memoria(i)
        
        valores_n.append(i)
        llamadas_sin_memoria.append(ejecucionsin)
        llamadas_con_memoria.append(ejecucion)
    print("ANÁLISIS DE LLAMADAS EN FIBONACCI")
    print("=" * 70)
    print(f"{'n':<3} | {'Sin memoria':>12} | {'Con memoria':>12}")
    print("-" * 35)
    for n, sin_memoria, con_memoria in zip(
        valores_n, llamadas_sin_memoria, llamadas_con_memoria
    ):
        print(f"{n:<3} | {sin_memoria:>12} | {con_memoria:>12}")
    # Análisis para búsqueda binaria con diferentes objetivos
    print("\n" + "#" * 70 + "\n")
    print("ANÁLISIS DE LLAMADAS EN BÚSQUEDA BINARIA")
    print("=" * 70)
    
    arreglo_fijo = list(range(0, 41))  # Arreglo de 1 a 40
    objetivos = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
    28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40] # 41 no existe en el arreglo
    
    print(f"Arreglo: {arreglo_fijo}")
    print(f"\n{'Objetivo':<10} | {'Total llamadas':>15}")
    print("-" * 27)
    
    for objetivo in objetivos:
        _, _, total_llamadas = busqueda_binaria_arbol(
            arreglo_fijo,
            objetivo,
            0,
            len(arreglo_fijo) - 1
        )
        
        print(f"{objetivo:<10} | {total_llamadas:>15}")
