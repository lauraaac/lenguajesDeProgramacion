

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
automata.addEstado("tkn_period", 1) #5 #tener en cuenta
automata.addEstado("tkn_integer", 1) #6
automata.addEstado("", 0) #7
automata.addEstado("tkn_str", 1) #8
automata.addEstado("", 0) #9
automata.addEstado("id", 1) #10
automata.addEstado("", 0) #11 se borra
automata.addEstado("tkn_assign", 1) #12
automata.addEstado("", 0) #13
automata.addEstado("tkn_less", 1) #14 
automata.addEstado("", 0) #15 se borra
automata.addEstado("token_dif", 1) #16 se borra
automata.addEstado("tkn_leq", 1) #17
automata.addEstado("", 0) #18
automata.addEstado("tkn_greater", 1) #19 #tener en ceunta que el = puede estar en ambos caminos. Considerar quitarlo del ASCCI
automata.addEstado("tkn_geq", 1) #20
automata.addEstado("", 0) #21
automata.addEstado("tkn_div", 1) #22
automata.addEstado("", 0) #23
automata.addEstado("tkn_comment", 1) #24
automata.addEstado("tkn_opening_par", 1) #25
automata.addEstado("tkn_closing_par", 1) #26
automata.addEstado("tkn_plus", 1) #27
automata.addEstado("", 0) #28
automata.addEstado("tkn_minus", 1) #29
automata.addEstado("tkn_closing_bra", 1) #30
automata.addEstado("tkn_opening_bra", 1) #31
automata.addEstado("tkn_times", 1) #32
automata.addEstado("tkn_equal", 1) #33
automata.addEstado("tkn_mod", 1) #34
automata.addEstado("tkn_neq", 1) #35 
automata.addEstado("tkn_semicolon", 1) #36
automata.addEstado("tkn_comma", 1) #37
automata.addEstado("tkn_question_mark", 1) #38 OJO

#NUMEROS
#Se agrega al estado 0 del automata las aristas que permiten pasar del estado "" a "" con UN número.
for i in range(48,58):
  automata.addArista(0, chr(i), 1)
  automata.addArista(1, chr(i), 1)
  automata.addArista(2, chr(i), 3)
  automata.addArista(3, chr(i), 3)

#ASCII
#Se agregan todas los caracteres de ASCII al estado 1 para llegar al estado 6 (tkn_integer)
for i in range(256):
  automata.addArista(1, chr(i), 6)
  automata.addArista(2, chr(i), 5)
  automata.addArista(3, chr(i), 4)
  automata.addArista(7, chr(i), 7)
  automata.addArista(13, chr(i), 14)
  automata.addArista(18, chr(i), 19) 
  automata.addArista(28,chr(i),12)  #assing
  automata.addArista(21, chr(i), 22)
  automata.addArista(23, chr(i), 23)
 
#PUNTO
#Se toma en cuenta para los token de tipo flotante.
automata.addArista(1, chr(46), 2)

#Manejo Strings ""
# " 
automata.addArista(0, chr(34), 7)
#Se agrega estado para finalizar el str y llega al estado (tkn_str)
automata.addArista(7, chr(34), 8)

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

#Caracteres especiales:

# _
automata.addArista(9, chr(95), 9)
# =
automata.addArista(0, chr(61), 28)

# ==
automata.addArista(28, chr(61), 33)

# !=
automata.addArista(0, chr(33)+chr(61), 35)

# < 
automata.addArista(0, chr(60), 13)

# <=
automata.addArista(13, chr(61), 17)

# >
automata.addArista(0, chr(62), 18)

# >=
automata.addArista(18, chr(61), 20)

# /
automata.addArista(0,  chr(92), 21)

# /
automata.addArista(21, chr(92), 23)

#LF nueva linea para comprobar que es un comentario
automata.addArista(23, chr(10), 24)

# (
automata.addArista(0, chr(40), 25)

# )
automata.addArista(0, chr(41), 26)

# +
automata.addArista(0, chr(43), 27)

# -
automata.addArista(0, chr(45), 29) 

# ]
automata.addArista(0, chr(93), 30)

# [
automata.addArista(0, chr(91), 31)

# *
automata.addArista(0, chr(42), 32)

# %
automata.addArista(0, chr(37), 34) 

# ;
automata.addArista(0,chr(59), 36)

# ,
automata.addArista(0, chr(44), 37)

# ,
automata.addArista(0, chr(44), 38)


#Salto de linea
automata.addArista(0, chr(10), 0)

automata.addArista(0, chr(13), 0) # ?

# cadena vacía
automata.addArista(0, " ", 0) 



input = sys.stdin.read()
input = "Put$"
newAnalizadorLexico = lexerAnalyser(automata, input)

     