from operator import ne
import re
import sys

ALPHABET_SIZE = 256


RESERVED_WORDS = {
    "AbsoluteValue",#d
    "and",#d
    "array",#d
    "decimal",
    "else",#d
    "elseif",#d
    "evaluates",
    "float",#d
    "for",#d
    "Function",
    "Get",#d
    "if",#d
    "input",#d
    "integer",#d
    "Main",
    "next",#d
    "not",#d
    "or",#d
    "output",#d
    "places",
    "Put",#d
    "RaiseToPower",#d
    "RandomNumber",#d
    "returns",#d
    "SeedRandomNumbers",#d
    "size",
    "SquareRoot",#d
    "to",#d
    "while",#d
    "with",
    "nothing"#d
}


episol = 'E'

contador = 0

class Token:
    def __init__(self, tipo, valor, fila, columna):
        self.tipo = tipo
        self.valor = valor
        self.fila = fila
        self.columna = columna

    def mostrarToken(self):
      if (self.valor == None):
        return "<"+ str(self.tipo)+","+str(self.fila)+","+str(self.columna)+">"
      else:
        return "<"+ str(self.tipo)+","+str(self.valor)+","+str(self.fila)+","+str(self.columna)+">"


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
    
    def getNextToken(self,lineas):

      while(self.scanner < len(self.codigo)):
      
        # Leer el caracter y mirar el indice de transición
        caracter_actual = self.codigo[self.scanner]
        
        ind = ord(caracter_actual)
        if ind == 8217:
          ind = 39

        # Se lee el estado al que la arista lleva.
        index = self.estado.aristas[ind] 

        # Si llegamos al final del input, leer un salto de linea
        if self.scanner == len(self.codigo)-1:
          index = self.estado.aristas[10]

        #print("estado:", aut.estado.key)

        # Verificar que exista transacción
        if index == -1:
        # print("kk")
          print(">>> Error lexico (linea: " + str(self.fila) + ", posicion: " + str(self.columna-len(self.lexema)) + ")")
          return -1
        else:
          #Se actualiza el estado al que lleva la arista
          self.estado = self.automata.estados[int(index)]

        # Actualizar los valores de fila y columna para cuando hay estados qaue necesitan de un caracter siguiente para determinar el  tipo de lexema
        if (self.estado.key != 11 and self.estado.key != 14 and self.estado.key != 17 and self.estado.key != 2 and self.estado.key != 7 and self.estado.key != 8 and self.estado.key != 6 and self.estado.key != 33 ):
      
          #si el caracter es un salto  de linea y un string vacion aumenta la fila y aumenta la columna
          if self.estado.key != 35 and self.estado.key != 36 and caracter_actual == chr(10): #pendiente
              #print("Esta", aut.estado.key)
              #print("SE ACTU FILA")
              self.fila = self.fila + 1
              self.columna = 1
          else:
            self.columna = self.columna + 1

        # Actualizar el valor de la cadena leida
        self.lexema = self.lexema + caracter_actual

        if ind == 92:
          if(self.codigo[self.scanner + 1] == '"'):
              self.columna = self.columna + 1
              self.scanner = self.scanner + 1
              self.lexema = self.lexema + '"'

        # Reiniciar el valor de la cadena luego de encontrar un token
        if self.estado.key == 0:
          self.lexema = ""

        # Si llegamos a un estado de aceptación
        if self.estado.aceptado == 1:
          # Aumentar o disminuir la posición sobre la que se está leyendo la cadena de entrada
          if self.estado.key != 11 and self.estado.key != 14 and self.estado.key != 17 and self.estado.key != 2 and self.estado.key != 7 and self.estado.key != 8 and self.estado.key != 6 and self.estado.key != 33 :
            self.scanner = self.scanner + 1
          else:
            if self.estado.key == 8:
              self.lexema = self.lexema[:-2]
              self.scanner = self.scanner - 1
              self.columna = self.columna - 1
            else:
              self.lexema = self.lexema[:-1]

          # Obtener posición inicial del lexema  
          tokenFila = self.fila
          tokenColumna = self.columna-len(self.lexema)
          tokenTipo = ""
          tokenLexema = ""

          # Crear Token
          if self.estado.tipoToken == "id":
            # Si es una palabra reservada
            if self.isReserved(self.lexema):

              tokenTipo = self.lexema
              self.estado = self.automata.getInit()
              self.lexema = ""
              crearToken = Token(tokenTipo,None, tokenFila, tokenColumna)
              return crearToken
            # Si no es palabra reservada
            else:
              tokenTipo = "id"
            
            tokenLexema = self.lexema

          # Se evalua los el si es cadena que imprima el formato sin comilla
          elif self.estado.tipoToken == "tkn_str":
            tokenTipo = self.estado.tipoToken
            tokenLexema = self.lexema[:-1][1:]
          
          # Se evalua que el token no sea un comentario para que pueda ser retornado
          elif self.estado.tipoToken != "tkn_comment":
            tokenTipo = self.estado.tipoToken
            tokenLexema = self.lexema

          elif self.estado.tipoToken == "tkn_comment":
          #print(lineas)
          #print("fila", aut.fila)
          #print("lexema", aut.lexema)
            if self.fila in lineas:
              crearToken = Token("tkn_div",None, tokenFila, tokenColumna)
              self.scanner = self.scanner-len(self.lexema)+1
              
              self.columna = self.columna-len(self.lexema)+1
              self.estado = self.automata.getInit()
              self.lexema = ""
              return crearToken
            else:
              self.fila = self.fila + 1
              self.columna = 1

          # Retornar token si no es un comentario
          if self.estado.tipoToken != "tkn_comment":

            if self.estado.tipoToken == "tkn_str" or self.estado.tipoToken == "id" or self.estado.tipoToken == "tkn_integer" or self.estado.tipoToken == "tkn_float":
              #print("lexm:", tokenLexema)
              #print("fil", aut.fila)
              crearToken = Token(tokenTipo, tokenLexema, tokenFila, tokenColumna)
              self.estado = self.automata.getInit()
              self.lexema = ""
              return crearToken
            else:
              # Regresar al estado inicial
              self.estado = self.automata.getInit()
              self.lexema = ""
              crearToken = Token(tokenTipo, None, tokenFila, tokenColumna)
              return crearToken

          # Regresar al estado inicial
          self.estado = self.automata.getInit()
          self.lexema = ""

        else:
          self.scanner = self.scanner + 1

      # Si llegamos al final del  input, entonces:
      if self.scanner == len(self.codigo):
        if self.estado.key != 0:
          print(">>> Error lexico (linea: " + str(self.fila) + ", posicion: " + str(self.columna-len(self.lexema)) + ")")
          return -1

        crearToken = Token("EOF", "EOF", self.fila + 1, 1)
        return crearToken

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
automata.addArista(0, chr(32), 0)
#automata.addArista(0, chr(36), 0)
automata.addArista(0, chr(10), 0)

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
  automata.addArista(1, chr(i), 1)

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




### Analizador Sintactico ###

class NoTerminal(object):

  def __init__(self, nombre, valor):
    self.valor = valor
    self.reglas = []
    self.nombre = nombre


class Gramatica(object):

  def __init__(self):
    self.cantidadNoTerminales = 0 
    self.noTerminales = []

  def getInit(self):
    return self.noTerminales[0]

  def addNoTerminal(self, nombre_noTerminal):
    newNoTerminal = NoTerminal(nombre_noTerminal, self.cantidadNoTerminales)
    self.noTerminales.append(newNoTerminal)
    self.cantidadNoTerminales = self.cantidadNoTerminales + 1
    return newNoTerminal

  def addRuleToNoTerminal(self, noTerminal, regla):
    self.noTerminales[noTerminal.valor].reglas.append(regla)

  def printgram(self):
    for A in self.noTerminales:
      for r in A.reglas:
        print(A.nombre, end=" -> ")
        for a in r:
          if type(a) is NoTerminal:
            print(a.nombre, end=" ")
          else:
            print(a, end=" ")
        print("")

class AnalizadorSintactico(object):

  def __init__(self, gram):
    self.gramatica = gram
    self.token = ""

  def getGram(self):
    return self.gramatica

  def getToken(self):
    return self.token

  def setImpr(self, token):

    if token == "tkn_integer":
      token = "integer_value"
    elif token == "tkn_float":
      token = "float_value"
    elif token == "tkn_str":
      token = "string_literal"
    elif token == "tkn_equal":
      token = "=="
    elif token == "tkn_assign":
      token = "="
    elif token == "tkn_geq":
      token = ">="
    elif token == "tkn_greater":
      token = ">"
    elif token == "tkn_leq":
      token = "<="
    elif token == "tkn_less":
      token = "<"
    elif token == "tkn_neq":
      token = "!="
    elif token == "tkn_period":
      token = "."
    elif token == "tkn_semicolon":
      token = ";"
    elif token == "tkn_closing_bra":
      token = "]"
    elif token == "tkn_opening_bra":
      token = "["
    elif token == "tkn_opening_par":
      token = "("
    elif token == "tkn_closing_par":
      token = ")"
    elif token == "tkn_minus":
      token = "-"
    elif token == "tkn_plus":
      token = "+"
    elif token == "tkn_times":
      token = "*"
    elif token == "tkn_mod":
      token = "%"
    elif token == "tkn_question_mark":
      token = "?"
    elif token == "tkn_div":
      token = "/"

    return token
  

  def primPerSymbol(self, simbolo):

    setPrimeros = set()
    if type(simbolo) is NoTerminal:
      for r in simbolo.reglas:
        setPrimeros |= self.primeros(r)
      return setPrimeros
    else:
      return {simbolo}
  
  def primeros(self, cadena):

    setPrimeros = set()
    if len(cadena) == 0:
      return {episol}
    else:
      if type(cadena[0]) is NoTerminal:
        prim = self.primPerSymbol(cadena[0])
        setPrimeros |= (prim - {episol}) 

        if episol in prim:
          if len(cadena) == 1:
            setPrimeros.add(episol)
          else:
            setPrimeros |= self.primeros(cadena[1:])
      else:
        return {cadena[0]}
    return setPrimeros

  def siguientes(self, noTerminal, terminals):
    setSiguientes = set()  
    terminals.add(noTerminal)

    if noTerminal == self.gramatica.getInit():
      setSiguientes.add("$")
      

    # Recorrer toda la gramatica en busca del no terminal
    for A in self.gramatica.noTerminales:
      for r in A.reglas:
        for i in range(len(r)):
          if r[i] == noTerminal:

            cadena = r[(i+1):]
            prim = self.primeros(cadena)
            setSiguientes |= (prim - {episol}) 

            if episol in prim and (A in terminals) == False:
              setSiguientes |= self.siguientes(A, terminals)   

    return setSiguientes

  def predict(self, noTerminal, rule):
    prim = self.primeros(rule)
    if episol in prim:
      return (prim - {episol}) | self.siguientes(noTerminal, set())
    else:
      return prim  

  def buildPredictionSets(self):
    for A in self.gramatica.noTerminales:
      for r in A.reglas:
        print(A.nombre, end=" -> ")
        for a in r:
          if type(a) is NoTerminal:
            print(a.nombre, end=" ")
          else:
            print(a, end=" ") 
        print("{ ", end="")
        for i in self.predict(A, r):
          if type(i) is NoTerminal:
            print(i.nombre, end=" ")
          else:
            print(i, end=" ")
        print("}")
  

  
  def emparejar(self, tokenEsperado, lineas):

    # print("token esperado", tokenEsperado)
    # print("valor token leido", self.token.valor)
    # print("tipo token", self.token.tipo)
    if self.token.tipo == tokenEsperado:
      print("EMPAREJADO: ", self.token.mostrarToken() )
      self.token = newAnalizadorLexico.getNextToken(lineas)
      return self.token
    else:
      print("<" + str(self.token.fila) + ":" + str(self.token.columna) + ">" + 
            " Error sintactico: se encontro: " + chr(34) + self.setImpr(self.token.tipo) + chr(34) + "; se esperaba: " + chr(34) + self.setImpr(tokenEsperado) + chr(34) + ".")
      return -1

  def A(self, noTerminal, lineas):
    respuesta = 0
    caso = True
    sets = set()
    # Evaluar para cada una de la reglas
    for r in noTerminal.reglas:

      setPredict = self.predict(noTerminal, r)

      #print("NO TERMINAL",noTerminal.nombre)
      if (self.getToken().tipo in setPredict) and caso:

        # Recorrer los elementos de la regla
        for a in r:
          if type(a) is NoTerminal:
            #print("no terminal en A kk", a.nombre)
            respuesta = self.A(a, lineas)
          elif a != "E":
            #print("no TERMINAL en prediccion", noTerminal.nombre)
            respuesta = self.emparejar(a, lineas)
          # Si hubo un error, retornamos
          if respuesta == -1:
            return -1
        # Hacer caso igual a False
        caso = False
      
      # Agregar conjunto de predicciones
      sets |= setPredict

    # Si no entro a ninguno de los casos
    if caso:
      if  self.token.tipo != "EOF":

        # Imprimir el error sintactico
        print("<" + str(self.token.fila) + ":" + str(self.token.columna) + ">" + 
              " Error sintactico: se encontro kk: " + chr(34) + self.setImpr(self.token.tipo) + chr(34) + "; se esperaba: ", end="")
        sets = list(sets)
        sets.sort()
        stringSets = ""
        for x in sets:
          stringSets = stringSets + chr(34) + self.setImpr(x) + chr(34) + ", "
        print(stringSets[:-2] + ".")

      return -1


#Se crea miniGramatica

gramaticaCoral = Gramatica()

PROGRAMA = gramaticaCoral.addNoTerminal("PROGRAMA")
DECLARACION = gramaticaCoral.addNoTerminal("DECLARACION")
DECLARACION2 = gramaticaCoral.addNoTerminal("DECLARACION2")
TIPO_VAR = gramaticaCoral.addNoTerminal("TIPO_VAR")
ARRAY = gramaticaCoral.addNoTerminal("ARRAY")
COMANDOS1 = gramaticaCoral.addNoTerminal("COMANDOS1")
ASIGNACION = gramaticaCoral.addNoTerminal("ASIGNACION")
ASIGNACION2 = gramaticaCoral.addNoTerminal("ASIGNACION2")
PUT = gramaticaCoral.addNoTerminal("PUT")
PUT2 = gramaticaCoral.addNoTerminal("PUT2")
OPERACION = gramaticaCoral.addNoTerminal("OPERACION")
OPERACION2 = gramaticaCoral.addNoTerminal("OPERACION2")
OP1 = gramaticaCoral.addNoTerminal("OP1")
VAR = gramaticaCoral.addNoTerminal("VAR")
SIGN = gramaticaCoral.addNoTerminal("SIGN")
TKN_INT = gramaticaCoral.addNoTerminal("TKN_INT")
TKN_FLT = gramaticaCoral.addNoTerminal("TKN_FLT")
ID1  = gramaticaCoral.addNoTerminal("ID1")
NOT = gramaticaCoral.addNoTerminal("NOT")
OPERATOR = gramaticaCoral.addNoTerminal("OPERATOR")
EXPRESION = gramaticaCoral.addNoTerminal("EXPRESION")
GET = gramaticaCoral.addNoTerminal("GET")
GET2 = gramaticaCoral.addNoTerminal("GET2")
DECLA_FUN = gramaticaCoral.addNoTerminal("DECLA_FUN")
PARAMS = gramaticaCoral.addNoTerminal("PARAMS")
PARAMS1 = gramaticaCoral.addNoTerminal("PARAMS1")
PARAMS2 = gramaticaCoral.addNoTerminal("PARAMS2")
FUNCION = gramaticaCoral.addNoTerminal("FUNCION")
CALL_FUNCION = gramaticaCoral.addNoTerminal("CALL_FUNCION")
WHILE = gramaticaCoral.addNoTerminal("WHILE")
WHILE_PARAM = gramaticaCoral.addNoTerminal("WHILE_PARAM")
IF = gramaticaCoral.addNoTerminal("IF")
IF_PARAM = gramaticaCoral.addNoTerminal("IF_PARAM")
ELSE = gramaticaCoral.addNoTerminal("ELSE")
ELSE_IF = gramaticaCoral.addNoTerminal("ELSE_IF")
FOR = gramaticaCoral.addNoTerminal("FOR")
FOR_PARAMS = gramaticaCoral.addNoTerminal("FOR_PARAMS")
ARRAY_ASIG = gramaticaCoral.addNoTerminal("ARRAY_ASIG")
LIST_TIPOS_ASIGNACION = gramaticaCoral.addNoTerminal("LIST_TIPOS_ASIGNACION")
LIST_PUT_VAR = gramaticaCoral.addNoTerminal("LIST_PUT_VAR")
LIST_ASIGNACION = gramaticaCoral.addNoTerminal("LIST_ASIGNACION")
COMANDOS_PROGRAMA = gramaticaCoral.addNoTerminal("COMANDOS_PROGRAMA")
MAIN = gramaticaCoral.addNoTerminal("MAIN")
LOGIC_OPERATION = gramaticaCoral.addNoTerminal("LOGIC_OPERATION")
LOGIC_OPERATION2 = gramaticaCoral.addNoTerminal("LOGIC_OPERATION2")
LOGIC_OPERATION3 = gramaticaCoral.addNoTerminal("LOGIC_OPERATION3")
LOGIC_OPERATOR = gramaticaCoral.addNoTerminal("LOGIC_OPERATOR")
LOGIC_OPERATOR2 = gramaticaCoral.addNoTerminal("LOGIC_OPERATOR2")
LOGIC_AND_OR = gramaticaCoral.addNoTerminal("LOGIC_AND_OR")
LISTA_OPERACIONES_SUB_PROCESO_IF = gramaticaCoral.addNoTerminal("LISTA_OPERACIONES_SUB_PROCESO")
LISTA_OPERACIONES_SUB_PROCESO_WHILE_FOR = gramaticaCoral.addNoTerminal("LISTA_OPERACIONES_SUB_PROCESO2")
BLOQUE_IF = gramaticaCoral.addNoTerminal("BLOQUE_IF")
SQUARE_ROOT   = gramaticaCoral.addNoTerminal("SQUARE_ROOT")
RAISE_TO_POWER   = gramaticaCoral.addNoTerminal("RAISE_TO_POWER")
ABSOLUTE_VALUE   = gramaticaCoral.addNoTerminal("ABSOLUTE_VALUE")
RANDOM_NUMBER   = gramaticaCoral.addNoTerminal("RANDOM_NUMBER")
SEED_RANDOM_NUMBER   = gramaticaCoral.addNoTerminal("SEED_RANDOM_NUMBER")
WITH   = gramaticaCoral.addNoTerminal("WITH")

#GRAMATICA FUNCIONES BUILTINS
gramaticaCoral.addRuleToNoTerminal(SQUARE_ROOT, ["SquareRoot","tkn_opening_par", OPERACION2, "tkn_closing_par"])
#gramaticaCoral.addRuleToNoTerminal(SQUARE_ROOT, [episol])
gramaticaCoral.addRuleToNoTerminal(RAISE_TO_POWER, ["RaiseToPower","tkn_opening_par", OPERACION2,"tkn_comma",OPERACION2,"tkn_closing_par"])
#gramaticaCoral.addRuleToNoTerminal(RAISE_TO_POWER, [episol])
gramaticaCoral.addRuleToNoTerminal(ABSOLUTE_VALUE, ["AbsoluteValue","tkn_opening_par", OPERACION2, "tkn_closing_par"])
#gramaticaCoral.addRuleToNoTerminal(ABSOLUTE_VALUE, [episol])
gramaticaCoral.addRuleToNoTerminal(RANDOM_NUMBER, ["RandomNumber","tkn_opening_par", OPERACION2,"tkn_comma",OPERACION2,"tkn_closing_par"])
#gramaticaCoral.addRuleToNoTerminal(RANDOM_NUMBER, [episol])
gramaticaCoral.addRuleToNoTerminal(SEED_RANDOM_NUMBER, ["SeedRandomNumbers","tkn_opening_par", OPERACION2,"tkn_closing_par"])
#gramaticaCoral.addRuleToNoTerminal(SEED_RANDOM_NUMBER, [episol])
#GRAMATICA FUNCION
gramaticaCoral.addRuleToNoTerminal(FUNCION,["Function", MAIN]) #ajustar funcion por no terminal
gramaticaCoral.addRuleToNoTerminal(MAIN, ["Main", "tkn_opening_par","tkn_closing_par","returns", "nothing" ])
#gramaticaCoral.addRuleToNoTerminal(FUNCION, [episol ])

gramaticaCoral.addRuleToNoTerminal(PROGRAMA, [COMANDOS_PROGRAMA])
gramaticaCoral.addRuleToNoTerminal(COMANDOS_PROGRAMA, [DECLARACION,COMANDOS_PROGRAMA])
gramaticaCoral.addRuleToNoTerminal(COMANDOS_PROGRAMA, [ASIGNACION,COMANDOS_PROGRAMA])
gramaticaCoral.addRuleToNoTerminal(COMANDOS_PROGRAMA, [PUT,COMANDOS_PROGRAMA])
gramaticaCoral.addRuleToNoTerminal(COMANDOS_PROGRAMA, [FUNCION]) #TODO: pendiente
gramaticaCoral.addRuleToNoTerminal(COMANDOS_PROGRAMA, [IF,COMANDOS_PROGRAMA])
gramaticaCoral.addRuleToNoTerminal(COMANDOS_PROGRAMA, [GET,COMANDOS_PROGRAMA])
gramaticaCoral.addRuleToNoTerminal(COMANDOS_PROGRAMA, [WHILE,COMANDOS_PROGRAMA])
gramaticaCoral.addRuleToNoTerminal(COMANDOS_PROGRAMA, [FOR,COMANDOS_PROGRAMA])
gramaticaCoral.addRuleToNoTerminal(COMANDOS_PROGRAMA, [SEED_RANDOM_NUMBER,COMANDOS_PROGRAMA])
gramaticaCoral.addRuleToNoTerminal(COMANDOS_PROGRAMA, [episol])


#LISTADO CASOS PARA EL SUBSTAMENT DE IF
gramaticaCoral.addRuleToNoTerminal(LISTA_OPERACIONES_SUB_PROCESO_IF, [DECLARACION,COMANDOS_PROGRAMA,BLOQUE_IF])
gramaticaCoral.addRuleToNoTerminal(LISTA_OPERACIONES_SUB_PROCESO_IF, [ASIGNACION,COMANDOS_PROGRAMA,BLOQUE_IF])
gramaticaCoral.addRuleToNoTerminal(LISTA_OPERACIONES_SUB_PROCESO_IF, [PUT,COMANDOS_PROGRAMA,BLOQUE_IF])
gramaticaCoral.addRuleToNoTerminal(LISTA_OPERACIONES_SUB_PROCESO_IF, [GET,COMANDOS_PROGRAMA,BLOQUE_IF])
gramaticaCoral.addRuleToNoTerminal(LISTA_OPERACIONES_SUB_PROCESO_IF, [IF,COMANDOS_PROGRAMA,BLOQUE_IF])
gramaticaCoral.addRuleToNoTerminal(LISTA_OPERACIONES_SUB_PROCESO_IF, [WHILE,COMANDOS_PROGRAMA,BLOQUE_IF])
gramaticaCoral.addRuleToNoTerminal(LISTA_OPERACIONES_SUB_PROCESO_IF, [FOR,COMANDOS_PROGRAMA,BLOQUE_IF])
gramaticaCoral.addRuleToNoTerminal(LISTA_OPERACIONES_SUB_PROCESO_IF, [SEED_RANDOM_NUMBER,COMANDOS_PROGRAMA,BLOQUE_IF])
gramaticaCoral.addRuleToNoTerminal(LISTA_OPERACIONES_SUB_PROCESO_IF, [BLOQUE_IF])

#LISTADO CASOS PARA EL SUBSTAMENT DE WHILE Y FOR
gramaticaCoral.addRuleToNoTerminal(LISTA_OPERACIONES_SUB_PROCESO_WHILE_FOR, [DECLARACION,COMANDOS_PROGRAMA])
gramaticaCoral.addRuleToNoTerminal(LISTA_OPERACIONES_SUB_PROCESO_WHILE_FOR, [ASIGNACION,COMANDOS_PROGRAMA])
gramaticaCoral.addRuleToNoTerminal(LISTA_OPERACIONES_SUB_PROCESO_WHILE_FOR, [PUT,COMANDOS_PROGRAMA])
gramaticaCoral.addRuleToNoTerminal(LISTA_OPERACIONES_SUB_PROCESO_WHILE_FOR, [GET,COMANDOS_PROGRAMA])
gramaticaCoral.addRuleToNoTerminal(LISTA_OPERACIONES_SUB_PROCESO_WHILE_FOR, [IF,COMANDOS_PROGRAMA])
gramaticaCoral.addRuleToNoTerminal(LISTA_OPERACIONES_SUB_PROCESO_WHILE_FOR, [WHILE,COMANDOS_PROGRAMA])
gramaticaCoral.addRuleToNoTerminal(LISTA_OPERACIONES_SUB_PROCESO_WHILE_FOR, [FOR,COMANDOS_PROGRAMA])
gramaticaCoral.addRuleToNoTerminal(LISTA_OPERACIONES_SUB_PROCESO_WHILE_FOR, [SEED_RANDOM_NUMBER,COMANDOS_PROGRAMA,BLOQUE_IF])

#GRAMATICA PARA IF
gramaticaCoral.addRuleToNoTerminal(IF,["if",IF_PARAM])
#gramaticaCoral.addRuleToNoTerminal(IF_PARAM,["tkn_opening_par",LOGIC_OPERATION2, "tkn_closing_par", LISTA_OPERACIONES_SUB_PROCESO_IF])
gramaticaCoral.addRuleToNoTerminal(IF_PARAM,[LOGIC_OPERATION2, LISTA_OPERACIONES_SUB_PROCESO_IF])

#GRAMATICA PARA ELSE
gramaticaCoral.addRuleToNoTerminal(ELSE, ["else",COMANDOS_PROGRAMA])
gramaticaCoral.addRuleToNoTerminal(ELSE, [episol])

#GRAMATICA PARA ELSEIF
gramaticaCoral.addRuleToNoTerminal(ELSE_IF, ["elseif", IF_PARAM])
gramaticaCoral.addRuleToNoTerminal(ELSE_IF, [episol])

gramaticaCoral.addRuleToNoTerminal(BLOQUE_IF, [ELSE_IF,ELSE])
gramaticaCoral.addRuleToNoTerminal(BLOQUE_IF, [episol])

#GRAMATICA PARA WHILE
gramaticaCoral.addRuleToNoTerminal(WHILE,["while",WHILE_PARAM])
#gramaticaCoral.addRuleToNoTerminal(WHILE_PARAM, ["tkn_opening_par",LOGIC_OPERATION2, "tkn_closing_par", LISTA_OPERACIONES_SUB_PROCESO_WHILE_FOR])
gramaticaCoral.addRuleToNoTerminal(WHILE_PARAM, [LOGIC_OPERATION2, LISTA_OPERACIONES_SUB_PROCESO_WHILE_FOR])

#GRAMATICA PARA FOR
gramaticaCoral.addRuleToNoTerminal(FOR, ["for", FOR_PARAMS])
gramaticaCoral.addRuleToNoTerminal(FOR_PARAMS, [ASIGNACION, "tkn_semicolon", LOGIC_OPERATION2,"tkn_semicolon",ASIGNACION,LISTA_OPERACIONES_SUB_PROCESO_WHILE_FOR])



gramaticaCoral.addRuleToNoTerminal(DECLARACION, [TIPO_VAR, ARRAY, "id"])
gramaticaCoral.addRuleToNoTerminal(TIPO_VAR, ["integer"])
gramaticaCoral.addRuleToNoTerminal(TIPO_VAR, ["float"])
gramaticaCoral.addRuleToNoTerminal(ARRAY, ["array"])
gramaticaCoral.addRuleToNoTerminal(ARRAY, [episol])
gramaticaCoral.addRuleToNoTerminal(LIST_TIPOS_ASIGNACION, ["id", ARRAY_ASIG])
gramaticaCoral.addRuleToNoTerminal(ARRAY_ASIG, ["tkn_opening_bra",OPERACION2 ,"tkn_closing_bra"])
gramaticaCoral.addRuleToNoTerminal(ARRAY_ASIG, [episol])

# EJ: x = 3+5 o x= Get next input
gramaticaCoral.addRuleToNoTerminal(LIST_ASIGNACION, [OPERACION2])
gramaticaCoral.addRuleToNoTerminal(LIST_ASIGNACION, [GET])
#gramaticaCoral.addRuleToNoTerminal(LIST_ASIGNACION, [ID1])

#EJ: x = something o x[2] = something
gramaticaCoral.addRuleToNoTerminal(ASIGNACION,[LIST_TIPOS_ASIGNACION, "tkn_assign",LIST_ASIGNACION]) #!añadir GET 


#EJ: Put "str" to output o Put kk to output o Put 3+4 to output
#gramaticaCoral.addRuleToNoTerminal(LIST_PUT_VAR, ["id"])
gramaticaCoral.addRuleToNoTerminal(LIST_PUT_VAR, ["tkn_str"])
gramaticaCoral.addRuleToNoTerminal(LIST_PUT_VAR, [OPERACION])

gramaticaCoral.addRuleToNoTerminal(WITH, ["with",TKN_INT,"places"])
gramaticaCoral.addRuleToNoTerminal(WITH, [episol])
gramaticaCoral.addRuleToNoTerminal(PUT, ["Put", LIST_PUT_VAR, "to", "output", WITH])

gramaticaCoral.addRuleToNoTerminal(VAR, [TKN_INT])
gramaticaCoral.addRuleToNoTerminal(VAR, [TKN_FLT])
gramaticaCoral.addRuleToNoTerminal(VAR, [ID1])
gramaticaCoral.addRuleToNoTerminal(VAR, [SQUARE_ROOT])
gramaticaCoral.addRuleToNoTerminal(VAR, [RAISE_TO_POWER])
gramaticaCoral.addRuleToNoTerminal(VAR, [ABSOLUTE_VALUE])
gramaticaCoral.addRuleToNoTerminal(VAR, [RANDOM_NUMBER])
gramaticaCoral.addRuleToNoTerminal(TKN_INT, ["tkn_integer"])
gramaticaCoral.addRuleToNoTerminal(TKN_FLT, ["tkn_float"])

# EJ: id o id(3,5) o id(3%5,x) 
gramaticaCoral.addRuleToNoTerminal(ID1, ["id", DECLA_FUN, ARRAY_ASIG])

#llamar funcion en asignacion
gramaticaCoral.addRuleToNoTerminal(PARAMS, [OPERACION,PARAMS1])
gramaticaCoral.addRuleToNoTerminal(PARAMS1, ["tkn_comma", OPERACION, PARAMS1 ])
gramaticaCoral.addRuleToNoTerminal(PARAMS1, [episol ])
gramaticaCoral.addRuleToNoTerminal(DECLA_FUN, ["tkn_opening_par", PARAMS, "tkn_closing_par", COMANDOS_PROGRAMA])
gramaticaCoral.addRuleToNoTerminal(DECLA_FUN, [episol])
#gramaticaCoral.addRuleToNoTerminal(CALL_FUNCION, ["id", "tkn_opening_par", PARAMS, "tkn_closing_par"])


gramaticaCoral.addRuleToNoTerminal(SIGN, ["tkn_plus"])
gramaticaCoral.addRuleToNoTerminal(SIGN, ["tkn_minus"])
gramaticaCoral.addRuleToNoTerminal(OPERATOR, ["tkn_plus",OPERACION])
gramaticaCoral.addRuleToNoTerminal(OPERATOR, ["tkn_minus",OPERACION])
gramaticaCoral.addRuleToNoTerminal(OPERATOR, ["tkn_div",OPERACION])
gramaticaCoral.addRuleToNoTerminal(OPERATOR, ["tkn_mod",OPERACION])
gramaticaCoral.addRuleToNoTerminal(OPERATOR, ["tkn_times",OPERACION])
gramaticaCoral.addRuleToNoTerminal(OPERATOR, [episol])
gramaticaCoral.addRuleToNoTerminal(OPERACION, ["tkn_opening_par", OPERACION2, "tkn_closing_par",OPERATOR])
gramaticaCoral.addRuleToNoTerminal(OPERACION2, ["tkn_opening_par", OPERACION2, "tkn_closing_par",OPERATOR])
gramaticaCoral.addRuleToNoTerminal(OPERACION2, [SIGN, OPERACION])
gramaticaCoral.addRuleToNoTerminal(OPERACION2, [VAR, OPERATOR])
gramaticaCoral.addRuleToNoTerminal(OPERACION, [SIGN, OPERACION])
gramaticaCoral.addRuleToNoTerminal(OPERACION, [VAR, OPERATOR])
gramaticaCoral.addRuleToNoTerminal(OPERACION, [episol])
gramaticaCoral.addRuleToNoTerminal(GET, ["Get", "next", "input"])
gramaticaCoral.addRuleToNoTerminal(LOGIC_OPERATION, ["not", "tkn_opening_par", LOGIC_OPERATION2,LOGIC_AND_OR, "tkn_closing_par", LOGIC_OPERATOR])
gramaticaCoral.addRuleToNoTerminal(LOGIC_OPERATION, [OPERACION, LOGIC_OPERATOR])
gramaticaCoral.addRuleToNoTerminal(LOGIC_OPERATION, [episol])

gramaticaCoral.addRuleToNoTerminal(LOGIC_OPERATION2, ["tkn_opening_par",LOGIC_OPERATION3,LOGIC_OPERATION2,LOGIC_AND_OR,"tkn_closing_par",LOGIC_OPERATOR])
gramaticaCoral.addRuleToNoTerminal(LOGIC_OPERATION2, ["not", "tkn_opening_par", LOGIC_OPERATION2,LOGIC_AND_OR, "tkn_closing_par", LOGIC_OPERATOR])
gramaticaCoral.addRuleToNoTerminal(LOGIC_OPERATION2, [OPERACION2, LOGIC_OPERATOR2,LOGIC_AND_OR])

gramaticaCoral.addRuleToNoTerminal(LOGIC_OPERATION3, [OPERACION, LOGIC_OPERATOR2,LOGIC_AND_OR])
gramaticaCoral.addRuleToNoTerminal(LOGIC_OPERATION2, [episol])

gramaticaCoral.addRuleToNoTerminal(LOGIC_OPERATOR, ["tkn_equal", LOGIC_OPERATION2])
gramaticaCoral.addRuleToNoTerminal(LOGIC_OPERATOR, ["tkn_geq",LOGIC_OPERATION2])
gramaticaCoral.addRuleToNoTerminal(LOGIC_OPERATOR, ["tkn_greater",LOGIC_OPERATION2])
gramaticaCoral.addRuleToNoTerminal(LOGIC_OPERATOR, ["tkn_neq",LOGIC_OPERATION2])
gramaticaCoral.addRuleToNoTerminal(LOGIC_OPERATOR, ["tkn_leq",LOGIC_OPERATION2])
gramaticaCoral.addRuleToNoTerminal(LOGIC_OPERATOR, ["tkn_less",LOGIC_OPERATION2])
gramaticaCoral.addRuleToNoTerminal(LOGIC_OPERATOR, [episol])


gramaticaCoral.addRuleToNoTerminal(LOGIC_AND_OR, ["and",LOGIC_OPERATION2])
gramaticaCoral.addRuleToNoTerminal(LOGIC_AND_OR, ["or",LOGIC_OPERATION2])
gramaticaCoral.addRuleToNoTerminal(LOGIC_AND_OR, [episol])

gramaticaCoral.addRuleToNoTerminal(LOGIC_OPERATOR2, ["tkn_equal", LOGIC_OPERATION])
gramaticaCoral.addRuleToNoTerminal(LOGIC_OPERATOR2, ["tkn_geq",LOGIC_OPERATION])
gramaticaCoral.addRuleToNoTerminal(LOGIC_OPERATOR2, ["tkn_greater",LOGIC_OPERATION])
gramaticaCoral.addRuleToNoTerminal(LOGIC_OPERATOR2, ["tkn_neq",LOGIC_OPERATION])
gramaticaCoral.addRuleToNoTerminal(LOGIC_OPERATOR2, ["tkn_leq",LOGIC_OPERATION])
gramaticaCoral.addRuleToNoTerminal(LOGIC_OPERATOR2, ["tkn_less",LOGIC_OPERATION])



#input = 'integer x Put "jaja" to output \n if ((3-5) < not(((3%4)== 3)) <= 5*(+-+-+9/x) == 0 or 2%(-+-+5) == 0)\n Put "vamos" to output \n elseif (x+3 < 3 and -(3)%(5) <= and -x+3 >= 5)\n Put 3+1 to output \n x = Get next input\n y = fun(x) y= 3*(x+ 4)%4 \n Put "eureka" to output \n else y[3%3] = Dios[0+y] + fun((3+2)) % prim()$' 
#input = 'if ((3-5) < not((3%4== 3)) <= 5*(9/x) == 0 or 2%(-+-+5) == 0)\n Put "vamos" to output \n elseif (x+3 < 3 and 3%5 <= and -x+3 >= 5)\n Put 3+1 to output$'
#input = 'integer kk \nkk = 0 \n   while (kk<=10) \n    Put kk to output Put "F" to output \n    if((k%2)==0 and not(k==4))     if(k==2)\n     x = kk \n    elseif(k==6) \n Put "x" to output \n x = fun(3,kk+3) \n y = Get next input while(y<x)\n z = y[2] + y[x+5] \n   for i=0; i>=10+p; i = i + 2 \n    Put "yep" to output \n    siu = Get next input$'
input = 'x = AbsoluteValue(0) if (x==1) Put "kk" to output with 3 places$'
print(input)
#input ='y = kk(x)$'
#input ='integer x$'
#ojito con x(3 == 4 ?
#input= 'if(not(3<5) and 3*5<= not(3+9==2)) Put "kk" to output $'
#ajustar caso x= l[0]
lineas = set()
newAnalizadorLexico = Analizador(automata, input)
newAnalizadorSintactico = AnalizadorSintactico(gramaticaCoral)

newAnalizadorSintactico.token = newAnalizadorLexico.getNextToken(lineas)
#print(newAnalizadorSintactico.token.mostrarToken())
#newAnalizadorSintactico.buildPredictionSets()
respuesta = newAnalizadorSintactico.A(gramaticaCoral.getInit(), lineas)
#print("respuesta", respuesta)
if respuesta != -1:
  print("El analisis sintactico ha finalizado exitosamente")
