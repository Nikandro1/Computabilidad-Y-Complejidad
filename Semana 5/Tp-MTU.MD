# TP — Máquina de Turing Universal

---

## 1. ¿Por qué se dice que una MTU es capaz de simular cualquier Máquina de Turing?

Porque está programada para recibir las instrucciones de la MT y ejecutarlas sobre la cadena que se le pasa. Toda MT tiene un conjunto finito de estados, símbolos y transiciones que se pueden codificar como una cadena `⟨M⟩`. La MTU recibe esa codificación junto con la entrada `w` y repite siempre el mismo ciclo: lee el estado actual, busca la transición que corresponde en `⟨M⟩` y la aplica. Como ese ciclo no depende de qué máquina esté simulando, funciona para cualquier MT.

---

## 2. MTU con M que acepta cadenas terminadas en 01

Hay que recibir la MT para que evalúe correctamente solamente cuando recibe `01` al final de la cadena. Deben estar programadas también las posibilidades de que se reciban las otras opciones y que la máquina las rechace.

La máquina si lee un `0` debe pasar al siguiente símbolo y si el siguiente es `1` debe marcar aceptado. En el caso contrario debe volver a leer la entrada o, en caso de no haber más símbolos, rechazarlo.

| Entrada | Resultado | Por qué |
|---|---|---|
| `U(⟨M⟩, 1101)` | **Acepta** | Termina en `01`, M llega al estado final |
| `U(⟨M⟩, 100)` | **Rechaza** | Termina en `00`, M no llega al estado final |
| `U(⟨M⟩, 01)` | **Acepta** | La cadena entera es `01`, M acepta |
| `U(⟨M⟩, 111)` | **Rechaza** | Termina en `11`, M nunca alcanza el estado final |

En el primer y tercer ejemplo nos da aceptado y en los demás rechazado. La MTU acepta si y solo si M acepta.

---

## 3. Análisis de la MT M

```
Q    0           1
q0   (q1,1,R)   (q1,0,R)
q1   (qf,0,R)   (qf,1,R)
qf   -           -
```

### A) ¿Qué hace M?

La M lee 2 símbolos. En el primer caso si lee `0` escribe `1` y viceversa. En el segundo estado deja el mismo símbolo que leyó y pasa al estado final donde la máquina para.

### B) ¿Qué información necesita la MTU para simular M?

- Necesita recibir los estados de M, cuál es el inicial y el final
- Los símbolos que utiliza (alfabeto)
- Las transiciones
- La configuración inicial: dónde comienza el cabezal y la cadena de entrada

### C) Codificación de la cinta de la MTU

La configuración `1 q0 0 1 1` significa que la cinta de M tiene `1 0 1 1`, el cabezal está sobre el `0` y el estado actual es `q0`.

**Convención de codificación:**

| Elemento | Código |
|---|---|
| q0 | 00 |
| q1 | 01 |
| qf | 10 |
| símbolo 0 | 0 |
| símbolo 1 | 1 |
| blanco □ | □ |
| R | 0 |
| L | 1 |

**Las 4 transiciones codificadas** (cada una ocupa 7 bits fijos):

```
(q0, lee 0) → (q1, escribe 1, R)  →  00 0 01 1 0  →  0000110
(q0, lee 1) → (q1, escribe 0, R)  →  00 1 01 0 0  →  0010100
(q1, lee 0) → (qf, escribe 0, R)  →  01 0 10 0 0  →  0101000
(q1, lee 1) → (qf, escribe 1, R)  →  01 1 10 1 0  →  0111010
```

**Cinta completa de la MTU:**

```
1*011 $ 000 # 0000110 # 0010100 # 0101000 # 0111010
```

Donde:
- `1*011` → cinta de M con `*` marcando la posición del cabezal
- `$` → separador
- `000` → estado actual q0 (`00`) + símbolo que lee (`0`)
- `#` → separador de transiciones
- Las 4 transiciones codificadas

---

## 4. Codificación de una máquina simple

Se define la MT que acepta cadenas terminadas en `01`.
 
**Convención de codificación binaria:**
 
Como la máquina tiene 5 estados, con 2 bits no alcanza (solo representa 4 combinaciones). Se usan 3 bits para los estados. Como hay 3 símbolos (0, 1 y blanco), se usan 2 bits para los símbolos.
 
```
Estados:   q0=000, q1=001, q2=010, q3=011, q4=100
Símbolos:  0=00,   1=01,   □=10
Dirección: R=0,    L=1
```
 
Cada transición ocupa 11 bits fijos:
```
estado actual (3) + símbolo lee (2) + nuevo estado (3) + símbolo escribe (2) + dirección (1)
```
 
**Transiciones codificadas:**
 
```
00000001000   → q0 lee 0 → q1, escribe 0, R
00001000010   → q0 lee 1 → q0, escribe 1, R
00010011100   → q0 lee □ → q3, escribe □, R
00100001000   → q1 lee 0 → q1, escribe 0, R
00101010010   → q1 lee 1 → q2, escribe 1, R
00110011100   → q1 lee □ → q3, escribe □, R
01000001000   → q2 lee 0 → q1, escribe 0, R
01001000010   → q2 lee 1 → q0, escribe 1, R
01010100100   → q2 lee □ → q4, escribe □, R
```
La cadena completa queda leyendo el estado q0 y el valor 0 y recibe la entrada 01
```
*01 $ 0000 # 00000001000 # 00001000010 # 00010011100 # 00100001000 # 00101010010 # 00110011100 # 01000001000 # 01001000010 # 01010100100
´´´

## 5. Simulación básica en Python

Se implementó un simulador que recibe la codificación de una MT y una cadena de entrada, y simula paso a paso su ejecución. El código se adjunta en el archivo `MTU.py`.

---

## 6. Pruebas de funcionamiento

| Entrada | Resultado esperado | Resultado obtenido |
|---|---|---|
| `[1, 1, 0, 1]` | Acepta | Acepta ✓ |
| `[1, 0, 0]` | Rechaza | Rechaza ✓ |
| `[0, 1]` | Acepta | Acepta ✓ |
| `[1, 1, 1]` | Rechaza | Rechaza ✓ |

```
=======================================================
INICIO DE SIMULACIÓN
Entrada w = [1, 1, 0, 1]
=======================================================

Paso   1 | Estado: q0
  Cinta:    [B][1][1][0][1][B]
  Cabezal:      ↑
  Regla: (0, 1) → estado=0, escribe=1, mueve=R →

Paso   2 | Estado: q0
  Cinta:    [B][1][1][0][1][B]
  Cabezal:         ↑
  Regla: (0, 1) → estado=0, escribe=1, mueve=R →

Paso   3 | Estado: q0
  Cinta:    [B][1][1][0][1][B]
  Cabezal:            ↑
  Regla: (0, 0) → estado=1, escribe=0, mueve=R →

Paso   4 | Estado: q1
  Cinta:    [B][1][1][0][1][B]
  Cabezal:               ↑
  Regla: (1, 1) → estado=2, escribe=1, mueve=R →

Paso   5 | Estado: q2
  Cinta:    [B][1][1][0][1][B][B]
  Cabezal:                  ↑
  Regla: (2, 2) → estado=4, escribe=2, mueve=R →

Paso   6 | Estado: q4
  Cinta:    [B][1][1][0][1][B][B][B]
  Cabezal:                     ↑

  ✓ Estado 4 es final → ACEPTA
=======================================================
  Entrada: [1, 1, 0, 1] | Resultado: ACEPTA | ✓ OK
```

---

## 7. Informe final

### Codificación utilizada

Se usó una codificación numérica donde los estados, símbolos y direcciones se representan como números enteros. Cada transición es una tupla de 5 elementos de tamaño fijo, lo que permite que la MTU sepa exactamente cuántos bits corresponden a cada campo.

### Ejemplos de ejecución


### Reflexión: MTU y computadoras modernas

La MTU y una computadora moderna funcionan de la misma manera:

| MTU | Computadora moderna |
|---|---|
| `⟨M⟩` (descripción de la MT) | El programa |
| `w` (la cadena de entrada) | Los datos |
| La MTU ejecutando | La CPU |
| La cinta | La memoria RAM |

La única diferencia es la velocidad y la escala. Una CPU ejecuta millones de instrucciones por segundo, pero el concepto es el mismo: leer una instrucción, ejecutarla y pasar a la siguiente.
