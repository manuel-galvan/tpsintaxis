import os
import pandas as pd
import analizadorsintactico as sintactico
import anytree as at
import numpy as np

class elemEstado:
  def __init__(self, id, tipo, valor, fila = 0, columna = 0):
    self.id = id
    self.tipo = tipo
    self.valor = valor
    self.fila = fila
    self.columna = columna

def recuperarEstado(idEstado, estado):
  i = 0
  while i < len(estado):
    if estado[i].id == id:
      return i
    else:
      i += 1
  raise Exception(f'No se definio la variable {idEstado}')

def analizadorSemantico(arbol):
  estado = []
  evalPrograma(arbol, estado)
  return estado

def asignarReal(arbol,estado,idVar):
  var = elemEstado(idVar, 'real', 0)
  estado.append(var)

def asignarMatriz(arbol, estado, nombre):
  fila = int(arbol.children[1].lexema)
  columna = int(arbol.children[3].lexema)
  if (fila <= 300 and fila >= 1) and (columna <= 300 and columna >= 1):
    valor = []
    while len(valor) < fila:
        col = []
        while len(col) < columna:
            col.append(0)
        valor.append(col)
    valor = np.matrix(valor)
    matriz = elemEstado(nombre, 'matriz', valor, fila, columna)
    estado.append(matriz)
  else:
     raise Exception('El tamaño maximo que una matriz puede tener es de 300 x 300')
  
def modificarVariableMatriz(estado, nombre, valor, fila, columna):
  i = recuperarEstado(nombre, estado)
  if (fila <= estado[i].fila) and (columna <= estado[i].columna):
    estado[i].valor[fila-1, columna-1] = valor

def modificarVariable(estado, nombre, valor):
  i = recuperarEstado(nombre, estado)
  estado[i].valor = valor

def modificarMatriz(estado):
  pass
 

def obtenerVar(arbol,estado,tipo,fil,col):
  pass
  
#<Programa>::= 'Program' 'id' <EspacioVariables> <Cuerpo>
def evalPrograma(arbol,estado):
  evalEspacioVariables(arbol.children[2],estado) # arbol aca tendria que ser el puntero hijo de EspacioVariable
  evalCuerpo(arbol.children[3],estado)

#<EspacioVariables>::= 'id' '=' <Variable> <EV1>

def evalEspacioVariables(arbol, estado):
   if not(arbol.is_leaf):
    idVar = arbol.children[0].lexema
    evalVariable(arbol.children[2],estado,idVar)
    evalEV1(arbol.children[3],estado)

#<EV1>::= <EspacioVariables> |  epsilon
def evalEV1(arbol,estado):
  if arbol.children[0].name == 'espaciovariables':
    evalEspacioVariables(arbol.children[0],estado)
  else:
    pass
    
#<Variable>::= ‘TipoReal' | ‘[‘ ‘constanteReal’ ‘,’ ‘constanteReal’ ‘]’ 
def evalVariable(arbol,estado,idVar):
  if arbol.children[0].lexema == 'real':
    asignarReal(arbol, estado,idVar)
  elif arbol.children[0].lexema =='[':
    asignarMatriz(arbol, estado,idVar)

#<Cuerpo>:: '{'<Cuerpo2>’}’
def evalCuerpo(arbol,estado):
  evalCuerpo2(arbol.children[1],estado)

#<Cuerpo2>::= <Sentencia> <aux1>
def evalCuerpo2(arbol,estado):
  if not(arbol.is_leaf):
    evalSentencia(arbol.children[0],estado)
    evalAux1(arbol.children[1],estado)
#<aux1>::= <Cuerpo2> | epsilon 
def evalAux1(arbol,estado):
  if arbol.name == 'epsilon':
    pass
  else:
    evalCuerpo2(arbol.children[0],estado)
#<Sentencia>::= <Asignacion> | <Lectura> | <Escritura> | <Si> | <Mientras>
def evalSentencia(arbol,estado):
  if arbol.children[0].name == 'asignacion':
    evalAsignacion(arbol.children[0],estado)
  elif arbol.children[0].name == 'lectura':
    evalLectura(arbol.children[0],estado)
  elif arbol.children[0].name == 'escritura':
    evalEscritura(arbol.children[0],estado)
  elif arbol.children[0].name == 'si':
    evalSi(arbol.children[0],estado)
  elif arbol.children[0].name == 'mientras':
    evalMientras(arbol.children[0],estado)
#<Lectura>::= 'peek’ ‘(' 'cadena' ',' 'id’ ’)'
def evalLectura(arbol, estado):
  idtipo = arbol.children[3]
  valEscribir = input(arbol.children[1].lexema)
  try:
    valEscribir = float(valEscribir)
  except:
    raise Exception('Se esperaba un real')
  i = recuperarEstado(idtipo, estado)
  estado[i].valor = valEscribir
    

#<Escritura>::= 'dump’ ‘(' <Lista> ')'
def evalEscritura(arbol,estado):
  evalLista(arbol.children[2],estado)
#<Lista>::= <VarLista><aux2>
def evalLista(arbol,estado):
  evalVarLista(arbol.children[0],estado)
  evalAux2(arbol.children[1],estado)
#<aux2> ::= ',' <Lista> | epsilon
def evalAux2(arbol,estado):
  if arbol.name=='epsilon':
    pass
  else:
    evalLista(arbol.children[0],estado)
#<VarLista>::= 'cadena' | <ExpArit>  }
def evalVarLista(arbol,estado):
  if arbol.name == 'exparit':
    val = evalExpArit(arbol.children[0],estado)
  elif arbol.name == 'cadena':
     pass
    
#<Mientras>::= 'While ' <Condicion>':' <Cuerpo>
def evalMientras(arbol, estado):
    # Evaluar la condición inicial
    valor = evalCondicion(arbol.children[1], estado)
    
    # Mientras la condición sea verdadera
    while valor:
        # Evaluar el cuerpo del bucle
        evalCuerpo(arbol.children[3], estado)
        
        # Re-evaluar la condición después de ejecutar el cuerpo
        valor = evalCondicion(arbol.children[1], estado)
  
  
#<Asignacion>::= 'id' <aux3>
def evalAsignacion(arbol,estado):
  nombre = arbol.children[0].lexema
  evalAux3(arbol.children[1],estado, nombre) 
#<aux3> ::=  '=' <ExpArit> | ‘[‘ <ExpArit> ‘,’ <ExpArit> ‘]’ ‘=’ <ExpArit>
def evalAux3(arbol,estado, nombre):
  if arbol.children[0].lexema == '=':  
    res = evalExpArit(arbol.children[1],estado)
    modificarVariable(estado, nombre, res)
    #asignarVar(variable,resultado)
  elif arbol.children[0].name == 'corcheteizq': #<---
    fila = evalExpArit(arbol.children[1],estado)
    col = evalExpArit(arbol.children[3],estado)
    constanteReal = evalExpArit(arbol.children[5],estado)
    modificarVariableMatriz(estado,nombre,constanteReal, fila, col)

#<ExpArit>::= <EAR1> <sub1> 
def evalExpArit(arbol,estado):
  op1 = evalEAR1(arbol.children[0],estado) 
  res = evalSub1(arbol.children[1],estado,op1)
  return res
  # devolver un resultado de EAR
	# las EAR deben devolver un resultado
   
#<sub1>::= ‘+’ <ExpArit> | ‘-’ <ExpArit> | epsilon
def evalSub1(arbol,estado,op1):
  if arbol.children[0].name == 'suma':
    op2 = evalExpArit(arbol.children[1],estado)
    res = op1 + op2
    return res
  elif arbol.children[0].name == 'menos':
    op2 = evalExpArit(arbol.children[1],estado)
    res = op1 - op2
    return res
  elif arbol.children[0].name == 'epsilon':
    return op1
  
#<EAR1>::= <EAR2> <sub2> 
def evalEAR1(arbol,estado):
  op1 = evalEAR2(arbol.children[0],estado)
  res = evalSub2(arbol.children[1],estado,op1)
  return res
#<sub2>::= ‘*’ <EAR1> | ‘/’ <EAR1> | epsilon
def evalSub2(arbol,estado,op1):
  if arbol.children[0].name == 'multiplicacion':
    op2 = evalEAR1(arbol.children[1],estado)
    res = op1 * op2
    return res
  elif arbol.children[0].name == 'division':
    op2 = evalEAR1(arbol.children[1],estado)
    res = op1 / op2
    return res
  elif arbol.children[0].name == 'epsilon':
    return op1
  
#<EAR2>::=  <EAR3> <sub3>
def evalEAR2(arbol,estado):
  op1 = evalEAR3(arbol.children[0],estado)
  res = evalSub3(arbol.children[1],estado,op1)
  return res
  i = 0


#<sub3>::= ‘^’ <EAR2> | epsilon
def evalSub3(arbol,estado,op1):
  op1 = int(op1.lexema)
  if arbol.children[0].name == 'epsilon':
    return op1
  elif arbol.children[0].name == 'potencia':
    op2 =int(evalEAR2(arbol.children[1],estado))
    op1 = op1 ** op2
    return op1

    
#<EAR3>::= '('<ExpArit>')' |  'Transpose’ ‘(' <ExpArit> ')' | 'Size’ ‘(' <ExpArit> ',' 'constantereal' ')' | ‘id’ <EAR4> | ‘ConstanteReal’ | ‘-’<EAR3> | <constanteMatriz>

def evalEAR3(arbol,estado):
  if arbol.children[0].name == 'constantereal':
    return arbol.children[0]
  elif arbol.children[0].name == 'constantematriz':
    return evalconstanteMatriz(arbol.children[0],estado)
  elif arbol.children[0].name == 'size':
    return evalExpArit(arbol.children[2],estado)
  elif arbol.children[0].name == 'transpose':
    return evalExpArit(arbol.children[2],estado)
  if arbol.children[0].name =='parentesisizq':
    return evalExpArit(arbol.children[1],estado)
  elif arbol.children[0].name == 'id':
    return evalEAR4(arbol.children[1],estado)
  elif arbol.children[0].name == 'menos':
    return evalEAR3(arbol.children[1],estado)

#<EAR4>::= ‘[‘ <ExpArit> ‘,’ <ExpArit> ‘]’ | epsilon 
def evalEAR4(arbol,estado):
  if arbol.children[0].name == 'epsilon':
    pass
  else:
    subFila = evalExpArit(arbol.children[1],estado)
    subCol = evalExpArit(arbol.children[3],estado)
  
#<constanteMatriz>::= ‘[‘ <Filas> ‘]’ 
def evalconstanteMatriz(arbol,estado):
  matriz=[]
  evalFilas(arbol.children[1],estado,matriz)
  return matriz
#<Filas>::=  ‘[‘<listaNumeros>’]’ <aux4>
def evalFilas(arbol,estado,matriz):
  fila=[]
  evalListaNumeros(arbol.children[1],estado,fila)
  matriz.append(fila)
  evalAux4(arbol.children[3],estado,matriz)
#<aux4>::= ‘,’ <Filas> | epsilon
def evalAux4(arbol,estado,matriz):
  if arbol.children[0].name=='epsilon':
    pass
  else:
    evalFilas(arbol.children[1],estado,matriz)
#<listaNumeros>::= ‘ConstanteReal’ <aux5> 
def evalListaNumeros(arbol,estado,fila):
  cReal= arbol.children[0]
  fila.append(cReal)
  evalAux5(arbol.children[1],estado,fila)
#<aux5>::= ‘,’ <listaNumeros> | epsilon
def evalAux5(arbol,estado,fila):
  if arbol.children[0].name=='epsilon':
    pass
  else:
    evalListaNumeros(arbol.children[1],estado,fila) 
#<Si>::= 'If ' <Condicion> ':' <Cuerpo> <Sii>
def evalSi(arbol,estado):
  evalCondicion(arbol.children[1],estado)
  evalCuerpo(arbol.children[3],estado)
  evalSii(arbol.children[4],estado)
#<Sii>::= 'else' ’:’ <Cuerpo> | 'elif' <Condicion> ':' <Cuerpo> <Sii> | epsilon
def evalSii(arbol,estado):
  if arbol.children[0].name=='else':
    evalCuerpo(arbol.children[2],estado)
  elif arbol.children[0].name=='elif':
    evalCondicion(arbol.children[1],estado)
    evalCuerpo(arbol.children[3],estado)
    evalCuerpo(arbol.children[4],estado)
  elif arbol.children[0].name=='epsilon':
    pass
#<Condicion>::= <COND1> <aux6> 
def evalCondicion(arbol,estado):
  val = evalCond1(arbol.children[0],estado)
  res = evalAux6(arbol.children[1], estado, val)
  return res

#        return (val or valor2)
#     elif operador == 'and':
#        return (val and valor2)
#  else:
#     return val 


  evalAux6(arbol.children[1],estado)
#<aux6>::= 'or' <Condicion> | epsilon
def evalAux6(arbol, estado, cond1):
  if arbol.children[0].name=='epsilon':
    return cond1
  else:
    cond2 = evalCondicion(arbol.children[1], estado)
    return (cond1 or cond2)
  
#<COND1>::= <COND2> <aux7> 
def evalCond1(arbol,estado):
  evalCond2(arbol.children[0],estado)
  evalAux7(arbol.children[1],estado)  
#<aux7>::= 'and' <COND1> | epsilon
def evalAux7(arbol,estado):
  if arbol.children[0].name=='epsilon':
    pass
  else:
  	evalCond1(arbol.children[1],estado)
#*  
#<COND2>::= ‘not’ <COND2> | <ExpArit> ‘opRelacional’ <ExpArit> | ‘{‘ <Condicion> ‘}’
def evalCond2(arbol,estado):
  if arbol.children[0].name=='not':
    evalCond2(arbol.children[1],estado)
  elif arbol.children[0].name=='exparit':
    evalExpArit(arbol.children[0],estado)
    evalExpArit(arbol.children[2],estado)
  elif arbol.children[0].name=='llaveizq':
    evalCondicion(arbol.children[1],estado)



if __name__ == "__main__":
  script_dir = os.path.dirname(__file__)
  file_path = os.path.join(script_dir, 'Codigo.txt')
  texto = open(file_path).read()
  texto = texto.lower()
  arbol, ccomplex = sintactico.analizadorSintactico(texto)
  if arbol:
    est = analizadorSemantico(arbol)
    for elemento in est:
      print(f'nombre = {elemento.id}')
      print(f'valor = {elemento.valor}')

# Traceback (most recent call last):
#   File "d:\Usuario\Galvan\Escritorio\Manu\tpsintaxis\analizadorsemantico.py", line 359, in <module>
#     est = analizadorSemantico(arbol)
#   File "d:\Usuario\Galvan\Escritorio\Manu\tpsintaxis\analizadorsemantico.py", line 26, in analizadorSemantico
#     evalPrograma(arbol, estado)
#     ~~~~~~~~~~~~^^^^^^^^^^^^^^^
#   File "d:\Usuario\Galvan\Escritorio\Manu\tpsintaxis\analizadorsemantico.py", line 68, in evalPrograma
#     evalCuerpo(arbol.children[3],estado)
#     ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "d:\Usuario\Galvan\Escritorio\Manu\tpsintaxis\analizadorsemantico.py", line 94, in evalCuerpo
#     evalCuerpo2(arbol.children[1],estado)
#     ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "d:\Usuario\Galvan\Escritorio\Manu\tpsintaxis\analizadorsemantico.py", line 99, in evalCuerpo2
#     evalSentencia(arbol.children[0],estado)
#     ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "d:\Usuario\Galvan\Escritorio\Manu\tpsintaxis\analizadorsemantico.py", line 110, in evalSentencia
#     evalAsignacion(arbol.children[0],estado)
#     ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "d:\Usuario\Galvan\Escritorio\Manu\tpsintaxis\analizadorsemantico.py", line 168, in evalAsignacion
#     evalAux3(arbol.children[1],estado, nombre)
#     ~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "d:\Usuario\Galvan\Escritorio\Manu\tpsintaxis\analizadorsemantico.py", line 172, in evalAux3
#     res = evalExpArit(arbol.children[1],estado)
#   File "d:\Usuario\Galvan\Escritorio\Manu\tpsintaxis\analizadorsemantico.py", line 183, in evalExpArit
#     op1 = evalEAR1(arbol.children[0],estado)
#   File "d:\Usuario\Galvan\Escritorio\Manu\tpsintaxis\analizadorsemantico.py", line 204, in evalEAR1
#     op1 = evalEAR2(arbol.children[0],estado)
#   File "d:\Usuario\Galvan\Escritorio\Manu\tpsintaxis\analizadorsemantico.py", line 223, in evalEAR2
#     res = evalSub3(arbol.children[1],estado,op1)
#   File "d:\Usuario\Galvan\Escritorio\Manu\tpsintaxis\analizadorsemantico.py", line 229, in evalSub3
#     op1 = int(op1.lexema)
#               ^^^^^^^^^^
# AttributeError: 'list' object has no attribute 'lexema'