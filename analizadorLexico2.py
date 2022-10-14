from ast import operator
from cgi import print_form
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
              if self.lexema[-1] == chr(10):

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

        crearToken = Token("EOF", "EOF", self.fila+1, 1)
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
    self.espacios = "" 
  
  # def getSort(self, sets):
      
  #   pri_element = list(map(lambda x : x[1],sets))
  #   for e in range(len(sets)):
    
  #   for e in range (len(pri_element)):

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
      #print(" EMPAREJADO: ", self.token.mostrarToken())
      self.token = newAnalizadorLexico.getNextToken(lineas)
      return self.token
    else:

      if self.token.tipo == "tkn_float" or self.token.tipo == "tkn_integer"or self.token.tipo == "id" or self.token.tipo == "tkn_str": 
        string = self.token.valor
        if self.token.tipo == "tkn_str":
          string = string.replace("\n", "\\n")
          string = string.replace( r'\'', "\\")
          string = string.replace("\n", "\\n")  

        print("<" + str(self.token.fila) + ":" + str(self.token.columna) + ">" + 
          " Error sintactico: se encontro: " + chr(34) + string + chr(34) + "; se esperaba: " + chr(34) + self.setImpr(tokenEsperado) + chr(34) + ".")
      elif self.token.tipo == "EOF":
        print("<" + str(self.token.fila) + ":" + str(self.token.columna) + ">" + 
          " Error sintactico: se encontro final de archivo; se esperaba: ", end="")
      else:
        print("<" + str(self.token.fila) + ":" + str(self.token.columna) + ">" + 
          " Error sintactico: se encontro: " + chr(34) + self.setImpr(self.token.tipo) + chr(34) + "; se esperaba: " + chr(34) + self.setImpr(tokenEsperado) + chr(34) + ".")

      return -1

  def A(self, noTerminal, lineas):
    respuesta = 0
    caso = True
    sets = set()
    # Evaluar para cada una de la reglas
    self.espacios =  self.espacios + "    "
    #print(self.espacios +  noTerminal.nombre +"{")
    for r in noTerminal.reglas:
      #print(self.espacios, end ="")
      #for i in r:
      #  if type(i) is NoTerminal:
      #    print(i.nombre, end = "")
      #  else:
      #    print(i, end = "")
      #print("")
      setPredict = self.predict(noTerminal, r)

      #print(self.espacios + "token: ", self.getToken().mostrarToken())
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
      #if  (self.token.tipo != "EOF") or (self.token.tipo == "EOF" and noTerminal.nombre == "LISTA_COMANDOS_PROGRAMA2_NOTNULL") or (self.token.tipo == "EOF" and noTerminal.nombre == "LISTA_COMANDOS_PROGRAMA1"):
      #print("tióooo", self.token.tipo)
      # Imprimir el error sintactico
      if self.token.tipo == "tkn_float" or self.token.tipo == "tkn_integer" or self.token.tipo == "id" or self.token.tipo == "tkn_str": 
        string = self.token.valor
        if self.token.tipo == "tkn_str":
          string = string.replace("\n", "\\n")
          string = string.replace( r'\'', "\\")
          string = string.replace("\n", "\\n") 
        print("<" + str(self.token.fila) + ":" + str(self.token.columna) + ">" + 
          " Error sintactico: se encontro: " + chr(34) + string + chr(34) + "; se esperaba: ", end="")
      elif self.token.tipo == "EOF":
        print("<" + str(self.token.fila) + ":" + str(self.token.columna) + ">" + 
          " Error sintactico: se encontro final de archivo; se esperaba: ", end="")
      
      else:
        print("<" + str(self.token.fila) + ":" + str(self.token.columna) + ">" + 
          " Error sintactico: se encontro: " + chr(34) + self.setImpr(self.token.tipo) + chr(34) + "; se esperaba: ", end="")
      sets = list(sets)
      stringSets = ""
      operators = [
        "tkn_equal",
        "tkn_assign", 
        "tkn_geq",
        "tkn_greater",
        "tkn_leq",
        "tkn_less",
        "tkn_neq",
        "tkn_period",
        "tkn_semicolon",
        "tkn_closing_bra",
        "tkn_opening_bra",
        "tkn_opening_par",
        "tkn_closing_par",
        "tkn_minus",
        "tkn_plus",
        "tkn_times",
        "tkn_mod",
        "tkn_question_mark",
        "tkn_div"
         ] 
      sortedsWords = []
      sortedOperators = []
      #print("BEFORE SORTING", sets)
      for x in sets:
        if x in operators:
          sortedOperators.append(x)
        else:
          sortedsWords.append(self.setImpr(x))

      
      sortedsWords = sorted(sortedsWords, key = str.lower)
      ##print("WORDS",sortedsWords)
      sortedOperators = sorted(sortedOperators)
      ##print("OPERATORS",sortedOperators)

      for x in sortedsWords:
        #print("word", x)
        stringSets = stringSets + chr(34) + x + chr(34) + ", "

      for x in sortedOperators:
        #print("operator", x)
        stringSets = stringSets + chr(34) + self.setImpr(x) + chr(34) + ", "

      print(stringSets[:-2] + ".")
      return -1

    #self.espacios =  self.espacios[:-4]

   # print(self.espacios + "}")


#Se crea miniGramatica

gramaticaCoral = Gramatica()

PROGRAMA = gramaticaCoral.addNoTerminal("PROGRAMA")

LISTA_COMANDOS_PROGRAMA = gramaticaCoral.addNoTerminal("LISTA_COMANDOS_PROGRAMA")
LISTA_COMANDOS_PROGRAMA1 = gramaticaCoral.addNoTerminal("LISTA_COMANDOS_PROGRAMA1")
LISTA_COMANDOS_PROGRAMA2_NOTNULL = gramaticaCoral.addNoTerminal("LISTA_COMANDOS_PROGRAMA2_NOTNULL")
LISTA_COMANDOS_PROGRAMA2 = gramaticaCoral.addNoTerminal("LISTA_COMANDOS_PROGRAMA2")
LISTA_COMANDOS_PROGRAMA3 = gramaticaCoral.addNoTerminal("LISTA_COMANDOS_PROGRAMA3")
LISTA_COMANDOS_PROGRAMA4 = gramaticaCoral.addNoTerminal("LISTA_COMANDOS_PROGRAMA4")
LISTA_COMANDOS_PROGRAMA5 = gramaticaCoral.addNoTerminal("LISTA_COMANDOS_PROGRAMA5")
LISTA_COMANDOS_PROGRAMA6 = gramaticaCoral.addNoTerminal("LISTA_COMANDOS_PROGRAMA6")
LISTA_COMANDOS_PROGRAMA7 = gramaticaCoral.addNoTerminal("LISTA_COMANDOS_PROGRAMA7")
LISTA_COMANDOS_PROGRAMA8 = gramaticaCoral.addNoTerminal("LISTA_COMANDOS_PROGRAMA8")

COMANDOS_PROGRAMA = gramaticaCoral.addNoTerminal("COMANDOS_PROGRAMA")
LISTA_FUNCIONES = gramaticaCoral.addNoTerminal("LISTA_FUNCIONES")
LISTA_FUNCIONES2 = gramaticaCoral.addNoTerminal("LISTA_FUNCIONES2")
LISTA_FUNCIONES3 = gramaticaCoral.addNoTerminal("LISTA_FUNCIONES3")
FUNCION = gramaticaCoral.addNoTerminal("FUNCION")
TIPO_VAR_FUN = gramaticaCoral.addNoTerminal("TIPO_VAR_FUN")
PARAMS_DECL_FUN = gramaticaCoral.addNoTerminal("PARAMS_DECL_FUN")
PARAMS_DECL_FUN2 = gramaticaCoral.addNoTerminal("PARAMS_DECL_FUN2")
MAIN = gramaticaCoral.addNoTerminal("MAIN")

DECLARACION = gramaticaCoral.addNoTerminal("DECLARACION")
TIPO_VAR = gramaticaCoral.addNoTerminal("TIPO_VAR")
ARRAY = gramaticaCoral.addNoTerminal("ARRAY")
ARRAY_DEF = gramaticaCoral.addNoTerminal("ARRAY_DEF")

ASIGNACION = gramaticaCoral.addNoTerminal("ASIGNACION")
ASIGNACION2 = gramaticaCoral.addNoTerminal("ASIGNACION2")
ASIGNACION3 = gramaticaCoral.addNoTerminal("ASIGNACION3")
LIST_ASIGNACION = gramaticaCoral.addNoTerminal("LIST_ASIGNACION")
LIST_ASIGNACION2 = gramaticaCoral.addNoTerminal("LIST_ASIGNACION2")
GET = gramaticaCoral.addNoTerminal("GET")

PUT = gramaticaCoral.addNoTerminal("PUT")
WITH   = gramaticaCoral.addNoTerminal("WITH")
LIST_PUT_VAR = gramaticaCoral.addNoTerminal("LIST_PUT_VAR")

IF = gramaticaCoral.addNoTerminal("IF")
ELSE_IF = gramaticaCoral.addNoTerminal("ELSE_IF")
ELSE = gramaticaCoral.addNoTerminal("ELSE")

WHILE = gramaticaCoral.addNoTerminal("WHILE")
FOR = gramaticaCoral.addNoTerminal("FOR")

SEED_RANDOM_NUMBER = gramaticaCoral.addNoTerminal("SEED_RANDOM_NUMBER")



OPERACION = gramaticaCoral.addNoTerminal("OPERACION")
OPERACION1 = gramaticaCoral.addNoTerminal("EXPRESION1")
T = gramaticaCoral.addNoTerminal("T")
LISTA_E = gramaticaCoral.addNoTerminal("LISTA_E")
E = gramaticaCoral.addNoTerminal("E")
OPERACION_LOG = gramaticaCoral.addNoTerminal("OPERACION_LOG")
T_LOG = gramaticaCoral.addNoTerminal("T_LOG")
OPERACION1_LOG = gramaticaCoral.addNoTerminal("OPERACION1_LOG")
LISTA_E_LOG = gramaticaCoral.addNoTerminal("LISTA_E_LOG")
E_LOG = gramaticaCoral.addNoTerminal("E_LOG")

SQUARE_ROOT = gramaticaCoral.addNoTerminal("SQUARE_ROOT")
RAISE_TO_POWER = gramaticaCoral.addNoTerminal("RAISE_TO_POWER")
ABSOLUTE_VALUE = gramaticaCoral.addNoTerminal("ABSOLUTE_VALUE")
RANDOM_NUMBER = gramaticaCoral.addNoTerminal("RANDOM_NUMBER")

ID1  = gramaticaCoral.addNoTerminal("ID1")
LIS_ID1  = gramaticaCoral.addNoTerminal("LIS_ID1")

DECLA_FUN = gramaticaCoral.addNoTerminal("DECLA_FUN")
ARRAY_ASIG = gramaticaCoral.addNoTerminal("ARRAY_ASIG")
PARAMS = gramaticaCoral.addNoTerminal("PARAMS")
PARAMS1 = gramaticaCoral.addNoTerminal("PARAMS1")

OPERATOR = gramaticaCoral.addNoTerminal("OPERATOR")


# LISTAS
gramaticaCoral.addRuleToNoTerminal(LISTA_COMANDOS_PROGRAMA, [COMANDOS_PROGRAMA, LISTA_COMANDOS_PROGRAMA])
gramaticaCoral.addRuleToNoTerminal(LISTA_COMANDOS_PROGRAMA, [episol])
gramaticaCoral.addRuleToNoTerminal(LISTA_COMANDOS_PROGRAMA1, [COMANDOS_PROGRAMA, LISTA_COMANDOS_PROGRAMA1])
gramaticaCoral.addRuleToNoTerminal(LISTA_COMANDOS_PROGRAMA1, [episol])
gramaticaCoral.addRuleToNoTerminal(LISTA_COMANDOS_PROGRAMA2_NOTNULL, [COMANDOS_PROGRAMA, LISTA_COMANDOS_PROGRAMA2])
gramaticaCoral.addRuleToNoTerminal(LISTA_COMANDOS_PROGRAMA2, [COMANDOS_PROGRAMA, LISTA_COMANDOS_PROGRAMA2])
gramaticaCoral.addRuleToNoTerminal(LISTA_COMANDOS_PROGRAMA2, [episol])
gramaticaCoral.addRuleToNoTerminal(LISTA_COMANDOS_PROGRAMA3, [COMANDOS_PROGRAMA, LISTA_COMANDOS_PROGRAMA3])
gramaticaCoral.addRuleToNoTerminal(LISTA_COMANDOS_PROGRAMA3, [episol])
gramaticaCoral.addRuleToNoTerminal(LISTA_COMANDOS_PROGRAMA4, [COMANDOS_PROGRAMA, LISTA_COMANDOS_PROGRAMA4])
gramaticaCoral.addRuleToNoTerminal(LISTA_COMANDOS_PROGRAMA4, [episol])
gramaticaCoral.addRuleToNoTerminal(LISTA_COMANDOS_PROGRAMA5, [COMANDOS_PROGRAMA, LISTA_COMANDOS_PROGRAMA5])
gramaticaCoral.addRuleToNoTerminal(LISTA_COMANDOS_PROGRAMA5, [episol])
gramaticaCoral.addRuleToNoTerminal(LISTA_COMANDOS_PROGRAMA6, [COMANDOS_PROGRAMA, LISTA_COMANDOS_PROGRAMA6])
gramaticaCoral.addRuleToNoTerminal(LISTA_COMANDOS_PROGRAMA6, [episol])
gramaticaCoral.addRuleToNoTerminal(LISTA_COMANDOS_PROGRAMA7, [COMANDOS_PROGRAMA, LISTA_COMANDOS_PROGRAMA7])
gramaticaCoral.addRuleToNoTerminal(LISTA_COMANDOS_PROGRAMA7, [episol])
gramaticaCoral.addRuleToNoTerminal(LISTA_COMANDOS_PROGRAMA8, [COMANDOS_PROGRAMA, LISTA_COMANDOS_PROGRAMA8])
gramaticaCoral.addRuleToNoTerminal(LISTA_COMANDOS_PROGRAMA8, [episol])

# PORGRAMA
gramaticaCoral.addRuleToNoTerminal(PROGRAMA, ["Function", LISTA_FUNCIONES, "EOF"])
gramaticaCoral.addRuleToNoTerminal(PROGRAMA, [LISTA_COMANDOS_PROGRAMA, "EOF"])
gramaticaCoral.addRuleToNoTerminal(LISTA_FUNCIONES, [FUNCION, LISTA_FUNCIONES2])
gramaticaCoral.addRuleToNoTerminal(LISTA_FUNCIONES2, ["Function", LISTA_FUNCIONES3])
gramaticaCoral.addRuleToNoTerminal(LISTA_FUNCIONES3, [LISTA_FUNCIONES])
gramaticaCoral.addRuleToNoTerminal(LISTA_FUNCIONES3, [MAIN])

# Comandos
gramaticaCoral.addRuleToNoTerminal(COMANDOS_PROGRAMA, [DECLARACION])
gramaticaCoral.addRuleToNoTerminal(COMANDOS_PROGRAMA, [ASIGNACION])
gramaticaCoral.addRuleToNoTerminal(COMANDOS_PROGRAMA, [PUT])
gramaticaCoral.addRuleToNoTerminal(COMANDOS_PROGRAMA, [IF])
gramaticaCoral.addRuleToNoTerminal(COMANDOS_PROGRAMA, [WHILE])
gramaticaCoral.addRuleToNoTerminal(COMANDOS_PROGRAMA, [FOR])
gramaticaCoral.addRuleToNoTerminal(COMANDOS_PROGRAMA, [SEED_RANDOM_NUMBER])

# Funcion
gramaticaCoral.addRuleToNoTerminal(FUNCION, ["id", "tkn_opening_par", PARAMS_DECL_FUN, "tkn_closing_par", "returns", TIPO_VAR_FUN, LISTA_COMANDOS_PROGRAMA1])
gramaticaCoral.addRuleToNoTerminal(TIPO_VAR_FUN, [DECLARACION])
gramaticaCoral.addRuleToNoTerminal(TIPO_VAR_FUN, ["nothing"])
gramaticaCoral.addRuleToNoTerminal(PARAMS_DECL_FUN, [TIPO_VAR, "id", PARAMS_DECL_FUN2])
gramaticaCoral.addRuleToNoTerminal(PARAMS_DECL_FUN, [episol])
gramaticaCoral.addRuleToNoTerminal(PARAMS_DECL_FUN2, ["tkn_comma", TIPO_VAR, "id", PARAMS_DECL_FUN2] )
gramaticaCoral.addRuleToNoTerminal(PARAMS_DECL_FUN2, [episol])

# Main
gramaticaCoral.addRuleToNoTerminal(MAIN, ["Main", "tkn_opening_par", "tkn_closing_par", "returns", "nothing", LISTA_COMANDOS_PROGRAMA2_NOTNULL])

# Declaracion
gramaticaCoral.addRuleToNoTerminal(DECLARACION, [TIPO_VAR, ARRAY, "id"])
gramaticaCoral.addRuleToNoTerminal(ARRAY, ["array", "tkn_opening_par", ARRAY_DEF, "tkn_closing_par"])
gramaticaCoral.addRuleToNoTerminal(TIPO_VAR, ["integer"])
gramaticaCoral.addRuleToNoTerminal(TIPO_VAR, ["float"])
gramaticaCoral.addRuleToNoTerminal(ARRAY, [episol])

gramaticaCoral.addRuleToNoTerminal(ARRAY_DEF, ["tkn_integer"])
gramaticaCoral.addRuleToNoTerminal(ARRAY_DEF, ["tkn_question_mark"])

# Asignacion
gramaticaCoral.addRuleToNoTerminal(ASIGNACION, ["id", ASIGNACION2]) 
gramaticaCoral.addRuleToNoTerminal(ASIGNACION2, [LIST_ASIGNACION2, "tkn_assign", LIST_ASIGNACION]) 
gramaticaCoral.addRuleToNoTerminal(ASIGNACION2, ["tkn_opening_par", PARAMS, "tkn_closing_par"]) 

gramaticaCoral.addRuleToNoTerminal(ASIGNACION3, ["id", LIST_ASIGNACION2, "tkn_assign", LIST_ASIGNACION]) 


gramaticaCoral.addRuleToNoTerminal(LIST_ASIGNACION2, ["tkn_opening_bra", OPERACION, "tkn_closing_bra"])
gramaticaCoral.addRuleToNoTerminal(LIST_ASIGNACION2, ["tkn_period", "size"])
gramaticaCoral.addRuleToNoTerminal(LIST_ASIGNACION2, [episol])

gramaticaCoral.addRuleToNoTerminal(LIST_ASIGNACION, [OPERACION])
gramaticaCoral.addRuleToNoTerminal(LIST_ASIGNACION, [GET])

# Get
gramaticaCoral.addRuleToNoTerminal(GET, ["Get", "next", "input"])

# Put
gramaticaCoral.addRuleToNoTerminal(PUT, ["Put", LIST_PUT_VAR, "to", "output", WITH])
gramaticaCoral.addRuleToNoTerminal(LIST_PUT_VAR, ["tkn_str"])
gramaticaCoral.addRuleToNoTerminal(LIST_PUT_VAR, [OPERACION])
gramaticaCoral.addRuleToNoTerminal(WITH, ["with", OPERACION, "decimal", "places"])
gramaticaCoral.addRuleToNoTerminal(WITH, [episol])

# If
gramaticaCoral.addRuleToNoTerminal(IF, ["if", OPERACION_LOG, LISTA_COMANDOS_PROGRAMA3, ELSE_IF, ELSE])
gramaticaCoral.addRuleToNoTerminal(ELSE_IF, ["elseif", OPERACION_LOG, LISTA_COMANDOS_PROGRAMA4])
gramaticaCoral.addRuleToNoTerminal(ELSE_IF, [episol])
gramaticaCoral.addRuleToNoTerminal(ELSE, ["else", LISTA_COMANDOS_PROGRAMA5])
gramaticaCoral.addRuleToNoTerminal(ELSE, [episol])

# While
gramaticaCoral.addRuleToNoTerminal(WHILE, ["while", OPERACION_LOG, LISTA_COMANDOS_PROGRAMA6])

# For
gramaticaCoral.addRuleToNoTerminal(FOR, ["for", ASIGNACION3, "tkn_semicolon", OPERACION_LOG, "tkn_semicolon", ASIGNACION3, LISTA_COMANDOS_PROGRAMA7])

# Seed_Random_Number
gramaticaCoral.addRuleToNoTerminal(SEED_RANDOM_NUMBER, ["SeedRandomNumbers", "tkn_opening_par", OPERACION, "tkn_closing_par"])


# Operacion

gramaticaCoral.addRuleToNoTerminal(OPERACION, [T, OPERACION1])
gramaticaCoral.addRuleToNoTerminal(OPERACION1, [OPERATOR, T, OPERACION1])
gramaticaCoral.addRuleToNoTerminal(OPERACION1, [episol])
gramaticaCoral.addRuleToNoTerminal(T, [E, LISTA_E])
gramaticaCoral.addRuleToNoTerminal(LISTA_E, [OPERATOR, E, LISTA_E])
gramaticaCoral.addRuleToNoTerminal(LISTA_E, [episol])

gramaticaCoral.addRuleToNoTerminal(E, ["tkn_opening_par", OPERACION, "tkn_closing_par"]) 
gramaticaCoral.addRuleToNoTerminal(E, [ID1])
gramaticaCoral.addRuleToNoTerminal(E, ["tkn_integer"]) 
gramaticaCoral.addRuleToNoTerminal(E, ["tkn_float"])  
gramaticaCoral.addRuleToNoTerminal(E, ["tkn_minus", OPERACION]) 
gramaticaCoral.addRuleToNoTerminal(E, ["tkn_plus", OPERACION]) 
gramaticaCoral.addRuleToNoTerminal(E, [SQUARE_ROOT])
gramaticaCoral.addRuleToNoTerminal(E, [RAISE_TO_POWER])
gramaticaCoral.addRuleToNoTerminal(E, [ABSOLUTE_VALUE])
gramaticaCoral.addRuleToNoTerminal(E, [RANDOM_NUMBER])


gramaticaCoral.addRuleToNoTerminal(OPERACION_LOG, [T_LOG, OPERACION1_LOG])
gramaticaCoral.addRuleToNoTerminal(OPERACION1_LOG, [OPERATOR, T_LOG, OPERACION1_LOG])
gramaticaCoral.addRuleToNoTerminal(OPERACION1_LOG, [episol])
gramaticaCoral.addRuleToNoTerminal(T_LOG, [E_LOG, LISTA_E_LOG])
gramaticaCoral.addRuleToNoTerminal(LISTA_E_LOG, [OPERATOR, E_LOG, LISTA_E_LOG])
gramaticaCoral.addRuleToNoTerminal(LISTA_E_LOG, [episol])

gramaticaCoral.addRuleToNoTerminal(E_LOG, ["tkn_opening_par", OPERACION_LOG, "tkn_closing_par"]) 
gramaticaCoral.addRuleToNoTerminal(E_LOG, ["not", "tkn_opening_par", OPERACION_LOG, "tkn_closing_par"])
gramaticaCoral.addRuleToNoTerminal(E_LOG, [ID1])
gramaticaCoral.addRuleToNoTerminal(E_LOG, ["tkn_integer"]) 
gramaticaCoral.addRuleToNoTerminal(E_LOG, ["tkn_float"])  
gramaticaCoral.addRuleToNoTerminal(E_LOG, ["tkn_minus", OPERACION_LOG]) 
gramaticaCoral.addRuleToNoTerminal(E_LOG, ["tkn_plus", OPERACION_LOG]) 
gramaticaCoral.addRuleToNoTerminal(E_LOG, [SQUARE_ROOT])
gramaticaCoral.addRuleToNoTerminal(E_LOG, [RAISE_TO_POWER])
gramaticaCoral.addRuleToNoTerminal(E_LOG, [ABSOLUTE_VALUE])
gramaticaCoral.addRuleToNoTerminal(E_LOG, [RANDOM_NUMBER])

gramaticaCoral.addRuleToNoTerminal(SQUARE_ROOT, ["SquareRoot", "tkn_opening_par", OPERACION, "tkn_closing_par"])
gramaticaCoral.addRuleToNoTerminal(RAISE_TO_POWER, ["RaiseToPower", "tkn_opening_par", OPERACION, "tkn_comma", OPERACION, "tkn_closing_par"])
gramaticaCoral.addRuleToNoTerminal(ABSOLUTE_VALUE, ["AbsoluteValue", "tkn_opening_par", OPERACION, "tkn_closing_par"])
gramaticaCoral.addRuleToNoTerminal(RANDOM_NUMBER, ["RandomNumber", "tkn_opening_par", OPERACION, "tkn_comma", OPERACION,"tkn_closing_par"])

gramaticaCoral.addRuleToNoTerminal(ID1, ["id", LIS_ID1])
gramaticaCoral.addRuleToNoTerminal(LIS_ID1, [DECLA_FUN])
gramaticaCoral.addRuleToNoTerminal(LIS_ID1, [ARRAY_ASIG])
gramaticaCoral.addRuleToNoTerminal(LIS_ID1, [episol])

gramaticaCoral.addRuleToNoTerminal(DECLA_FUN, ["tkn_opening_par", PARAMS, "tkn_closing_par"])
gramaticaCoral.addRuleToNoTerminal(ARRAY_ASIG, ["tkn_opening_bra", OPERACION ,"tkn_closing_bra"])

gramaticaCoral.addRuleToNoTerminal(PARAMS, [OPERACION, PARAMS1])
gramaticaCoral.addRuleToNoTerminal(PARAMS1, ["tkn_comma", OPERACION, PARAMS1])
gramaticaCoral.addRuleToNoTerminal(PARAMS1, [episol])

gramaticaCoral.addRuleToNoTerminal(OPERATOR, ["tkn_div"])
gramaticaCoral.addRuleToNoTerminal(OPERATOR, ["tkn_mod"])
gramaticaCoral.addRuleToNoTerminal(OPERATOR, ["tkn_times"])
gramaticaCoral.addRuleToNoTerminal(OPERATOR, ["tkn_geq"])
gramaticaCoral.addRuleToNoTerminal(OPERATOR, ["tkn_greater"])
gramaticaCoral.addRuleToNoTerminal(OPERATOR, ["tkn_leq"])
gramaticaCoral.addRuleToNoTerminal(OPERATOR, ["tkn_less"])
gramaticaCoral.addRuleToNoTerminal(OPERATOR, ["tkn_plus"])
gramaticaCoral.addRuleToNoTerminal(OPERATOR, ["tkn_minus"])
gramaticaCoral.addRuleToNoTerminal(OPERATOR, ["tkn_neq"])
gramaticaCoral.addRuleToNoTerminal(OPERATOR, ["tkn_neq"])
gramaticaCoral.addRuleToNoTerminal(OPERATOR, ["tkn_equal"])
gramaticaCoral.addRuleToNoTerminal(OPERATOR, ["or"])
gramaticaCoral.addRuleToNoTerminal(OPERATOR, ["and"])

#input = 'for i = 0;\n    i < 5;\n\n                     i = i + 1\n   \n   Put i to output\n\n// ¡Ay! Olvidé declarar i\n\ninteger i\ntry_again(for_loop, i)\n\n// Menos mal que por ahora\n// No miramos la semántica\n\n$'
input = sys.stdin.read()+ '$'

lineas = set()
newAnalizadorLexico = Analizador(automata, input)
newAnalizadorSintactico = AnalizadorSintactico(gramaticaCoral)

newAnalizadorSintactico.token = newAnalizadorLexico.getNextToken(lineas)
respuesta = newAnalizadorSintactico.A(gramaticaCoral.getInit(), lineas)
if respuesta != -1:
  print("El analisis sintactico ha finalizado exitosamente.")