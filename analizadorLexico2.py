
import sys


ALPHABET_SIZE = 256

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

class Token:
    def __init__(self, tipo, valor, fila, columna):
        self.tipo = tipo
        self.valor = valor
        self.fila = fila
        self.columna = columna

    def mostrarToken(self):
        print("<"+ str(self.tipo)+","+str(self.valor)+","+str(self.fila)+","+str(self.columna)+">")


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

  def addEstado(self, tipoToken, aceptado):
    newEstado = Estado(self.cantidadEstados, tipoToken, aceptado)
    self.estados.append(newEstado)
    self.cantidadEstados = self.cantidadEstados + 1

  #Permite llevar de un estado a otro por medio de un elemento.
  def addArista(self, key1, c, key2):
    self.estados[key1].aristas[ord(c)] = key2 
  
  def printAut(self):
    for x in self.estados:
      print("Estado:", x.key)
      for i in range(ALPHABET_SIZE):
        if x.aristas[i] != 0:
          print("   Arista:", x.aristas[i], chr(i))
      if x.tipoToken != "":
        print("  ", x.tipoToken)

class Analizador(object):

    def __init__(self, automata, codigo):
      self.codigo = codigo

      self.scanner = 0 
      self.fila = 1
      self.columna = 1
      self.lexema = ""

      self.automata = automata
      self.estado = automata.getInit()


    def isReserved(self, nombreLexema):
      for x in RESERVED_WORDS:
        if nombreLexema == x:
          return True
      return False

    

# se crea el automata
automata = Automata()
automata.addEstado("", 0) #0
automata.addEstado("", 0) #1
automata.addEstado("id", 1) #2
automata.addEstado("", 0) #3
automata.addEstado("", 0) #4
automata.addEstado("", 0) #5
automata.addEstado("tkn_float", 1) #6
automata.addEstado("tkn_integer", 1) #7
automata.addEstado("tkn_integer", 1) #8

###  Parte automata que genera ids y tkn_float o tkn_integer


#ascii para pasar del estado 1 al 2 
for i in range(256):
  automata.addArista(1, chr(i), 2)

#Letras mayúsculas

for i in range(65,91):
  automata.addArista(0, chr(i), 1)

  #bucle de letras mayusculas y se sobreescribe las aristas de estado 1
  automata.addArista(1, chr(i), 1)

#Letras minúsculas
for i in range(97, 123):
   automata.addArista(0, chr(i), 1)

   #bucle de letras minúsculas y se sobreescribe las aristas de estado 1
   automata.addArista(1, chr(i), 1)

# caracter "_" para ids
automata.addArista(1, chr(95),1)

### Parte para identificar tkn de números

for i in range(256):
  automata.addArista(3, chr(i), 7)

#números
for i in range(48,58):
  automata.addArista(0, chr(i),3)

  #bucle de números
  automata.addArista(3, chr(i),3)

# caracter "." para floats
automata.addArista(3, chr(46),4)

#letras para despues de leer un punto o para depues de leer un número
for i in range(256):
  automata.addArista(4, chr(i), 8)
  automata.addArista(5, chr(i), 6)

#número para después de leer un punto
for i in range(48,58):
  automata.addArista(4, chr(i),5)

  #bucle de números
  automata.addArista(5, chr(i),5)

automata.addEstado("", 0) #9
automata.addEstado("tkn_equal", 1) #10
automata.addEstado("tkn_assign", 1) #11
automata.addEstado("", 0) #12
automata.addEstado("tkn_leq", 1) #13
automata.addEstado("tkn_less", 1) #14 
automata.addEstado("", 0) #15
automata.addEstado("tkn_geq", 1) #16
automata.addEstado("tkn_greater", 1) #17
automata.addEstado("", 0) #18
automata.addEstado("tkn_neq", 1) #19

#ASCII para despues de leer un =
for i in range(256):
  automata.addArista(9, chr(i), 11)
  automata.addArista(12, chr(i), 14)
  automata.addArista(15, chr(i), 17)

# caracter "="
automata.addArista(0, chr(61),9)

#caracter "<"
automata.addArista(0, chr(60),12)

#caracter ">"
automata.addArista(0, chr(62),15)

#caracter "!"
automata.addArista(0, chr(33),18)

# Se agregan las segundas partes de los operadores para verificar
automata.addArista(9, chr(61),10) # "=="
automata.addArista(12, chr(61), 13) #"<="
automata.addArista(15, chr(61), 16) #">="
automata.addArista(18, chr(61), 19) #"!="



## parte de automata para identificar caracteres especiales de lenguaje
automata.addEstado("tkn_period", 1) #20
automata.addEstado("tkn_comma", 1) #21
automata.addEstado("tkn_semicolon", 1) #22
automata.addEstado("tkn_closing_bra", 1) #23
automata.addEstado("tkn_opening_bra", 1) #24
automata.addEstado("tkn_opening_par", 1) #25
automata.addEstado("tkn_closing_par", 1) #26
automata.addEstado("tkn_minus", 1) #27
automata.addEstado("tkn_plus", 1) #28
automata.addEstado("tkn_times", 1) #29
automata.addEstado("tkn_mod", 1) #30
automata.addEstado("tkn_question_mark", 1) #31

# caracter "."
automata.addArista(0, chr(46),20)
# caracter ","
automata.addArista(0, chr(44),21)
# caracter ";"
automata.addArista(0, chr(59),22)
# caracter "]"
automata.addArista(0, chr(93),23)
# caracter "["
automata.addArista(0, chr(91),24)
# caracter "("
automata.addArista(0, chr(40),25)
# caracter ")"
automata.addArista(0, chr(41),26)
# caracter "-"
automata.addArista(0, chr(45),27)
# caracter "+"
automata.addArista(0, chr(43),28)
# caracter "*"
automata.addArista(0, chr(42),29)
# caracter "%"
automata.addArista(0, chr(37),30)
# caracter "?"
automata.addArista(0, chr(63),31)

### parte del automata para encontrar comentarios o string

automata.addEstado("", 0) #32
automata.addEstado("tkn_div", 1) #33
automata.addEstado("", 0) #34
automata.addEstado("tkn_comment", 1) #35
automata.addEstado("", 0) #36
automata.addEstado("tkn_str", 1) #37

# caracter "/"
automata.addArista(0, chr(47),32)

#caracter " " "
automata.addArista(0, chr(34),36)

for i in range(256):
  automata.addArista(32, chr(i),33)

# caracter "/"
automata.addArista(32, chr(47),34)

#ASCII para leer caracteres luego de iniciar un comentrio
for i in range(256):
  automata.addArista(34, chr(i),34)

automata.addArista(34, chr(10), 35)

#ASCII para leer caracteres luego de iniciar un string
for i in range(256):
  automata.addArista(36, chr(i),36)

automata.addArista(36, chr(34),37)
