BLANCO = 2  # Símbolo especial para celda vacía


def crear_maquina(transiciones, estado_inicial, estados_finales):
    return {
        "transiciones": transiciones,
        "estado_inicial": estado_inicial,
        "estados_finales": estados_finales,
    }


def simular(maquina, entrada, max_pasos=1000, verbose=True):

    transiciones   = maquina["transiciones"]
    estado_final   = maquina["estados_finales"]
    estado_actual  = maquina["estado_inicial"]

    cinta = {i: s for i, s in enumerate(entrada)}
    cabezal = 0 

    if verbose:
        print("=" * 55)
        print("INICIO DE SIMULACIÓN")
        print(f"Entrada w = {entrada}")
        print("=" * 55)


    for paso in range(1, max_pasos + 1):

        # 1. Leer el símbolo bajo el cabezal (blanco si la celda no existe)
        simbolo_leido = cinta.get(cabezal, BLANCO)

        if verbose:
            _imprimir_configuracion(paso, estado_actual, cinta, cabezal)

        # 2. Buscar la transición en ⟨M⟩
        clave = (estado_actual, simbolo_leido)
        if clave not in transiciones:
            # No hay regla → la máquina para
            if verbose:
                print(f"\n  ✗ No hay transición para {clave}")
                print(f"  Estado actual {'es final → ACEPTA' if estado_actual in estado_final else 'NO es final → RECHAZA'}")
                print("=" * 55)
            return estado_actual in estado_final


        nuevo_estado, simbolo_escrito, direccion = transiciones[clave]

        if verbose:
            dir_str = "R →" if direccion == 1 else "← L"
            print(f"  Regla: ({estado_actual}, {simbolo_leido}) "
                  f"→ estado={nuevo_estado}, escribe={simbolo_escrito}, mueve={dir_str}")


        cinta[cabezal] = simbolo_escrito


        cabezal += 1 if direccion == 1 else -1


        estado_actual = nuevo_estado


        if estado_actual in estado_final:
            if verbose:
                _imprimir_configuracion(paso + 1, estado_actual, cinta, cabezal)
                print(f"\n  ✓ Estado {estado_actual} es final → ACEPTA")
                print("=" * 55)
            return True


    if verbose:
        print(f"\n  ⚠ Límite de {max_pasos} pasos alcanzado → posible ciclo infinito")
        print("=" * 55)
    return False


def _imprimir_configuracion(paso, estado, cinta, cabezal):
    """Imprime la configuración actual de la cinta."""
    if not cinta:
        return
    min_pos = min(min(cinta.keys()), cabezal) - 1
    max_pos = max(max(cinta.keys()), cabezal) + 1

    contenido = ""
    indicador = ""
    for pos in range(min_pos, max_pos + 1):
        simbolo = cinta.get(pos, BLANCO)
        s = "B" if simbolo == BLANCO else str(simbolo)
        contenido += f"[{s}]"
        if pos == cabezal:
            indicador += " ↑ "
        else:
            indicador += "   "

    print(f"\nPaso {paso:>3} | Estado: q{estado}")
    print(f"  Cinta:    {contenido}")
    print(f"  Cabezal:  {indicador}")



def maquina_del_tp():
    """
    MT del punto 3 del TP:
    Complementa el primer bit y deja el segundo igual.

    Estados: q0=0, q1=1, qf=2
    Símbolos: 0=0, 1=1, Blanco=2
    Direcciones: L=0, R=1
    """
    transiciones = {
        (0, 0): (1, 1, 1),   # q0 lee 0 → escribe 1, R, va a q1
        (0, 1): (1, 0, 1),   # q0 lee 1 → escribe 0, R, va a q1
        (1, 0): (2, 0, 1),   # q1 lee 0 → escribe 0, R, va a qf
        (1, 1): (2, 1, 1),   # q1 lee 1 → escribe 1, R, va a qf
    }
    return crear_maquina(transiciones, estado_inicial=0, estados_finales={2})


def maquina_termina_en_01():
    """
    MT que acepta cadenas que terminan en 01.
    Recorre toda la cinta buscando ese sufijo.

    Estados:
        q0 = inicio / reset
        q1 = leí un 0, espero un 1
        q2 = leí 01 → estado de aceptación
        q3 = rechazo (estado trampa)

    Esta versión lee la cadena de izquierda a derecha y trackea
    los últimos dos símbolos vistos usando los estados.
    """
    transiciones = {
        # Desde q0 (inicio o después de ver algo que no fue 0)
        (0, 0): (1, 0, 1),   # veo 0, puede ser inicio de 01 → q1
        (0, 1): (0, 1, 1),   # veo 1, no sirve como inicio → sigo en q0

        # Desde q1 (el símbolo anterior fue 0)
        (1, 0): (1, 0, 1),   # veo otro 0, el nuevo 0 puede ser inicio → q1
        (1, 1): (2, 1, 1),   # veo 1 después de 0 → ¡encontré 01! → q2 (aceptación)

        # Desde q2 (ya vi 01, pero sigo leyendo para ver si es el final)
        (2, 0): (1, 0, 1),   # viene otro 0, puede haber un 01 posterior
        (2, 1): (0, 1, 1),   # viene un 1, el 01 ya no está al final → reset

        # Blanco = fin de cinta
        (0, BLANCO): (3, BLANCO, 1),   # terminé sin 01 al final → rechaza
        (1, BLANCO): (3, BLANCO, 1),   # terminé con 0 al final, no 01 → rechaza
        (2, BLANCO): (4, BLANCO, 1),   # terminé justo después de 01 → acepta
    }
    return crear_maquina(transiciones, estado_inicial=0, estados_finales={4})



def pruebas_maquina_tp():
    print("\n" + "█" * 55)
    print("  PRUEBAS: MT del punto 3 (complementa primer bit)")
    print("█" * 55)

    M = maquina_del_tp()
    casos = [
        [0, 0],   # espera: cinta → 1,0
        [1, 1],   # espera: cinta → 0,1
        [0, 1],   # espera: cinta → 1,1
        [1, 0],   # espera: cinta → 0,0
    ]
    for entrada in casos:
        simular(M, entrada, verbose=True)
        print()


def pruebas_termina_en_01():
    print("\n" + "█" * 55)
    print("  PRUEBAS: MT que acepta cadenas terminadas en 01")
    print("█" * 55)

    M = maquina_termina_en_01()
    casos = [
        ([1, 1, 0, 1], True),    # 1101 → acepta
        ([1, 0, 0],    False),   # 100  → rechaza
        ([0, 1],       True),    # 01   → acepta
        ([1, 1, 1],    False),   # 111  → rechaza
    ]
    for entrada, esperado in casos:
        resultado = simular(M, entrada, verbose=True)
        estado = "✓ OK" if resultado == esperado else "✗ FALLO"
        print(f"  Entrada: {entrada} | Resultado: {'ACEPTA' if resultado else 'RECHAZA'} | {estado}\n")



if __name__ == "__main__":
    print("\nElegí qué probar:")
    print("  1. MT del punto 3 del TP")
    print("  2. MT que acepta cadenas terminadas en 01")
    print("  3. Ambas")
    opcion = input("\nOpción (1/2/3): ").strip()

    if opcion == "1":
        pruebas_maquina_tp()
    elif opcion == "2":
        pruebas_termina_en_01()
    else:
        pruebas_maquina_tp()
        pruebas_termina_en_01()