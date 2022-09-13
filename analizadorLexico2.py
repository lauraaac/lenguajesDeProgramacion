

ALPHABET_SIZE = 256

NUMBERS = "0123456789"

RESERVED_WORDS = {
    "AbsoluteValue",
    "and",
    "array",
    "decimal",
    "else",
    "elseif",
    "evaluates",
    "float",
    "for",
    "Function",
    "Get",
    "if",
    "input",
    "integer",
    "Main",
    "next",
    "not",
    "or",
    "output",
    "places",
    "Put",
    "RaiseToPower",
    "RandomNumber",
    "returns",
    "SeedRandomNumbers",
    "size",
    "SquareRoot",
    "to",
    "while",
    "with",
    "places",
    "nothing"
}

SPECIAL_CHARS_REGEX = r'[A-Za-z][A-Za-z0-9_]*'
NUMBERS_REGEX = r'[0-9]+'
FLOAT_REGEX = r'[0-9]+\.[0-9]+'

OPERATOR_SYMBOLS_TOKENS = {
    "-": "minus",
    ",": "comma",
    ";": "semicolon",
    "!=": "neq",
    "?": "question_mark",
    ".": "period",
    "(": "opening_par",
    ")": "closing_par",
    "[": "opening_bra",
    "]": "closing_bra",
    "*": "times",
    "/": "div",
    "%": "mod",
    "+": "plus",
    "<": "less",
    "<=": "leq",
    "=": "assign",
    "==": "equal",
    ">": "greater",
    ">=": "geq",
}

class Token:
    def __init__(self, tipo, valor, fila, columna):
        self.tipo = tipo
        self.valor = valor
        self.fila = fila
        self.columna = columna

    def mostrarToken(self):
        print(self.tipo, self.valor, self.fila, self.columna)


#Se definen los estados que crea un automata para el análisis de léxemas

class Estado():

  def __init__(self, key, tipoToken, aceptado):
    self.key = key
    self.tipoToken = tipoToken
    self.aceptado = aceptado
    self.aristas = []

#Cada estado tendrá alphabet_size aristas con valor -1
    for i in range(ALPHABET_SIZE):
      self.aristas.append(-1)


class Automata():

  def __init__(self):
    self.cantidadEstados = 0
    self.estados = []

  def getInit(self):
    return self.estados[0]

  def addEstado(self, tipoToken, accepted):
    newEstado = Estado(self.cantidadEstados, tipoToken, accepted)
    self.estados.append(newEstado)
    self.cantidadEstados = self.cantidadEstados + 1

  #Permite llevar de un estado a otro por medio de un elemento.
  def addArista(self, key1, c, key2):
    self.estados[key1].aristas[ord(c)] = key2 



# se crea el automata
automata = Automata()
automata.addEstado("", 0) #0
automata.addEstado("", 0) #1
automata.addEstado("", 0) #2 
automata.addEstado("", 0) #3 
automata.addEstado("tkn_float", 1) #4
automata.addEstado("tkn_integer", 1) #5
automata.addEstado("tkn_integer", 1) #6
automata.addEstado("", 0) #7
automata.addEstado("tkn_str", 1) #8

#NUMEROS
#Se agrega al estado 0 del automata las aristas que permiten pasar del estado "" a "" con UN número.
for i in range(48,58):
  automata.addArista(0, chr(i), 1)

#ASCII
#Se agregan todas los caracteres de ASCII al estado 1 para llegar al estado 6 (tkn_integer)
for i in range(256):
  automata.addArista(1, chr(i), 6)

#NÚMEROS
#Se agregan todos los número en el estado 1 y permiten llegar de nuevo al estado 1 para generar un entero gigante :v .
for i in range(48,58):
  automata.addArista(1, chr(i), 1)

#PUNTO
#Se toma en cuenta para los token de tipo flotante.
automata.addArista(1, chr(46), 2)

#ASCII
#Se agregan los caracteres de ASCII al estado 2 para llegar al estado 5 (tkn_integer)
for i in range(256):
  automata.addArista(2, chr(i), 5)

#NÚMERO
#Se agregan los números desde el estado 2 al 3 para determinar si realmente es un flotante.
for i in range(48, 58):
  automata.addArista(2, chr(i), 3)


#ASCII
#Se agregan ASCII  de estado 3 a 4 (tkn_float)
for i in range(255):
  automata.addArista(3, chr(i), 4)

#NÚMEROS
#Se agregan los bucles en el estado tres con los números
for i in range(48,58):
  automata.addArista(3, chr(i), 3)


# " 
automata.addArista(0, chr(34), 7)

# ''
#automata.addArista(0, chr(39), 7)

#ASCII
#Se agrega el alfabeto para trabajar los strings
for i in range(255):
  automata.addArista(7, chr(i), 7)

# "
#Se agrega estado para finalizar el str y llega al estado (tkn_str)
automata.addArista(7, chr(34), 8)

# ''
#automata.addArista(7, chr(39), 8)


automata.addEstado("", 0) #9
automata.addEstado("id", 1) #10
automata.addEstado("token_neg", 1) #11
automata.addEstado("token_igual", 1) #12


#letras en mayúscula a estado "" y bucle de estos
for i in range(65, 91):
  automata.addArista(0, chr(i), 9)
  automata.addArista(9, chr(i), 9)

#letras en minuscula a estado "" y bucle de estos
for i in range(97, 123):
  automata.addArista(0, chr(i), 9)
  automata.addArista(9, chr(i), 9)

#NÚMEROS
#Bucle de números para nombrar un id
for i in range(48,58):
  automata.addArista(9, chr(i), 9)

#ASCII
#todos los caracteres van al estado de id
for i in range(256):
  automata.addArista(9, chr(i), 10)

  

automata.addArista(9, "_", 9)

automata.addArista(0, "~", 11)

automata.addArista(0, "=", 12)

automata.addEstado("", 0) #13
automata.addEstado("token_menor", 1) #14
automata.addEstado("token_asig", 1) #15
automata.addEstado("token_dif", 1) #16
automata.addEstado("token_menor_igual", 1) #17

automata.addArista(0, "<", 13)

for i in range(256):
  automata.addArista(13, chr(i), 14)

automata.addArista(13, "-", 15)

automata.addArista(13, ">", 16)

automata.addArista(13, "=", 17)

automata.addEstado("", 0) #18
automata.addEstado("token_mayor", 1) #19
automata.addEstado("token_mayor_igual", 1) #20
automata.addEstado("", 0) #21
automata.addEstado("token_div", 1) #22
automata.addEstado("", 0) #23
automata.addEstado("token_comentario", 1) #24

automata.addArista(0, ">", 18)

for i in range(256):
  automata.addArista(18, chr(i), 19)
automata.addArista(18, "=", 20)

automata.addArista(0, "/", 21)

for i in range(256):
  automata.addArista(21, chr(i), 22)
automata.addArista(21, "/", 23)

for i in range(256):
  automata.addArista(23, chr(i), 23)
automata.addArista(23, chr(10), 24)

automata.addEstado("token_par_izq", 1) #25
automata.addEstado("token_par_der", 1) #26
automata.addEstado("token_mas", 1) #27
automata.addEstado("token_o", 1) #28
automata.addEstado("token_menos", 1) #29
automata.addEstado("token_cor_der", 1) #30
automata.addEstado("token_cor_izq", 1) #31
automata.addEstado("token_mul", 1) #32
automata.addEstado("token_y", 1) #33
automata.addEstado("token_mod", 1) #34
automata.addEstado("token_pot", 1) #35
automata.addEstado("token_pyc", 1) #36
automata.addEstado("token_coma", 1) #37
automata.addEstado("token_dosp", 1) #38

automata.addArista(0, "(", 25)
automata.addArista(0, ")", 26)
automata.addArista(0, "+", 27)
automata.addArista(0, "|", 28)
automata.addArista(0, "-", 29)
automata.addArista(0, "]", 30)
automata.addArista(0, "[", 31)
automata.addArista(0, "*", 32)
automata.addArista(0, "&", 33)
automata.addArista(0, "%", 34)
automata.addArista(0, "^", 35)
automata.addArista(0, ";", 36)
automata.addArista(0, ",", 37)
automata.addArista(0, ":", 38)

automata.addArista(0, chr(10), 0)
automata.addArista(0, chr(13), 0)
automata.addArista(0, " ", 0)



input = sys.stdin.read()
input = "Put$"
newAnalizadorLexico = lexerAnalyser(automata, input)

     