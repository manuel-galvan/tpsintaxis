import os
import pandas as pd
import analizadorsintactico as sintactico
import anytree as at
import numpy as np
# estado es lo que usamos como variables 
class elemEstado:# es necesario agregar lexema?
# porque si se puede usar es necesario tener la raiz de parametro para: evaloperacion, asignarReal y asignarMatriz
  def __init__(self, id, tipo, valor, fila = 0, columna = 0):
    self.id = id
    self.tipo = tipo
    self.valor = valor
    self.fila = fila
    self.columna = columna

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
  
def modificarReal(arbol,estado):
  pass

def modificarMatriz():
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
  if not(arbol.is_leaf):
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
  valEscribir = input(arbol.children[2].lexema) 
  #estado.asignarValor(arbol.children[4].lexema, valEscribir)
  #asigno a la variable a la que id haga referencia el valor de valEscribir
  #ciertaFuncion(estado,arbol.children[4],valEscribir)   #guardar el valor de id en estado

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

def modificarVariable(estado, nombre, valor):
  for variable in estado:
    if variable.id == nombre:
      variable.valor = valor
     
  
  
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
  elif arbol.children[0].name == 'corcheteizq':
    evalExpArit(arbol.children[1],estado)
    evalExpArit(arbol.children[3],estado)
    evalExpArit(arbol.children[5],estado,res)

#<ExpArit>::= <EAR1> <sub1> 
def evalExpArit(arbol,estado):
  op1 = evalEAR1(arbol.children[0],estado) 
  res = evalSub1(arbol.children[1],estado,op1)
  return res
  # devolver un resultado de EAR
	# las EAR deben devolver un resultado
   
#<sub1>::= ‘+’ <ExpArit> | ‘-’ <ExpArit> | epsilon
def evalSub1(arbol,estado,op1):
  op1 = int(op1.lexema)
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
  return evalSub2(arbol.children[1],estado,op1)
#<sub2>::= ‘*’ <EAR1> | ‘/’ <EAR1> | epsilon
def evalSub2(arbol,estado,op1):
  op1 = op1.lexema
  op1 = int(op1)
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
  return evalSub3(arbol.children[1],estado,op1)
  
#<sub3>::= ‘^’ <EAR2> | epsilon
def evalSub3(arbol,estado,op1):
  op1 = op1.lexema
  op1 = int(op1)
  if arbol.children[0].name == 'potencia':
    op2 = evalEAR2(arbol.children[1],estado).lexema
    op2 = int(op2)
    op1 = op1 ** op2
    return op1
  elif arbol.children[0].name == 'epsilon':
    return op1
    
#<EAR3>::= '('<ExpArit>')' |  'Transpose’ ‘(' <ExpArit> ')' | 'Size’ ‘(' <ExpArit> ',' 'constantereal' ')' | ‘id’ <EAR4> | ‘ConstanteReal’ | ‘-’<EAR3> | <constanteMatriz>

def evalEAR3(arbol,estado):
  if arbol.children[0].name == 'constantereal':
    return arbol.children[0]
  if arbol.children[1].name =='exparit':
    evalExpArit(arbol.children[1],estado)
  elif arbol.children[0].name == 'size':
    evalExpArit(arbol.children[2],estado)
  elif arbol.children[0].name == 'transpose':
    evalExpArit(arbol.children[2],estado)
  elif arbol.children[1].name == 'ear4':
    evalEAR4(arbol.children[1],estado)
  elif arbol.children[1].name == 'ear3':
    evalEAR4(arbol.children[1],estado)
  elif arbol.children[1].name == 'constantematriz':
    evalconstanteMatriz(arbol.children[0],estado)
#<EAR4>::= ‘[‘ <ExpArit> ‘,’ <ExpArit> ‘]’ | epsilon 
def evalEAR4(arbol,estado):
  if arbol.children[0].name == 'epsilon':
    pass
  else:
    evalEAR4(arbol.children[1],estado)
  
#<constanteMatriz>::= ‘[‘ <Filas> ‘]’ 
def evalconstanteMatriz(arbol,estado):
  evalFilas(arbol.children[1],estado)
#<Filas>::=  ‘[‘<listaNumeros>’]’ <aux4>
def evalFilas(arbol,estado):
  evalListaNumeros(arbol.children[1],estado)
  evalAux4(arbol.children[3],estado)
#<aux4>::= ‘,’ <Filas> | epsilon
def evalAux4(arbol,estado):
  if arbol.children[0].name=='epsilon':
    pass
  else:
    evalFilas(arbol.children[1],estado)
#<listaNumeros>::= ‘ConstanteReal’ <aux5> 
def evalListaNumeros(arbol,estado):
  evalAux5(arbol.children[1],estado)
#<aux5>::= ‘,’ <listaNumeros> | epsilon
def evalAux5(arbol,estado):
  if arbol.children[0].name=='epsilon':
    pass
  else:
    evalListaNumeros(arbol.children[1],estado)  
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

#  if arbol.children[1].name != 'epsilon':
#     operador = arbol.children[0].name
#     valor2 = evalCondicion(arbol.children[1].children[1], estado) 
#     if operador == 'or':
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
  arbol = sintactico.analizadorSintactico(texto)
  if arbol:
    est = analizadorSemantico(arbol)
    for elemento in est:
      print(f'nombre= {elemento.id}')
      print(f'valor= {elemento.valor}')
  
  
# Traceback (most recent call last):
#   File "c:\Users\Manu\Desktop\manolo\paiton\trabajo_practico_sintaxis\analizadorsemantico.py", line 343, in <module>
#     est = analizadorSemantico(arbol)
#           ^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "c:\Users\Manu\Desktop\manolo\paiton\trabajo_practico_sintaxis\analizadorsemantico.py", line 18, in analizadorSemantico
#     evalPrograma(arbol, estado)
#   File "c:\Users\Manu\Desktop\manolo\paiton\trabajo_practico_sintaxis\analizadorsemantico.py", line 55, in evalPrograma
#     evalCuerpo(arbol.children[3],estado)
#   File "c:\Users\Manu\Desktop\manolo\paiton\trabajo_practico_sintaxis\analizadorsemantico.py", line 83, in evalCuerpo
#     evalCuerpo2(arbol.children[1],estado)
#   File "c:\Users\Manu\Desktop\manolo\paiton\trabajo_practico_sintaxis\analizadorsemantico.py", line 88, in evalCuerpo2
#     evalSentencia(arbol.children[0],estado)
#   File "c:\Users\Manu\Desktop\manolo\paiton\trabajo_practico_sintaxis\analizadorsemantico.py", line 99, in evalSentencia
#     evalAsignacion(arbol.children[0],estado)
#   File "c:\Users\Manu\Desktop\manolo\paiton\trabajo_practico_sintaxis\analizadorsemantico.py", line 158, in evalAsignacion
#     evalAux3(arbol.children[1],estado, nombre)
#     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "c:\Users\Manu\Desktop\manolo\paiton\trabajo_practico_sintaxis\analizadorsemantico.py", line 162, in evalAux3        
#     res = evalExpArit(arbol.children[1],estado)
#           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "c:\Users\Manu\Desktop\manolo\paiton\trabajo_practico_sintaxis\analizadorsemantico.py", line 172, in evalExpArit     
#     op1 = evalEAR1(arbol.children[0],estado)
#           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "c:\Users\Manu\Desktop\manolo\paiton\trabajo_practico_sintaxis\analizadorsemantico.py", line 193, in evalEAR1        
#     op1 = evalEAR2(arbol.children[0],estado)
#           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "c:\Users\Manu\Desktop\manolo\paiton\trabajo_practico_sintaxis\analizadorsemantico.py", line 212, in evalEAR2        
#     res = evalSub3(arbol.children[1],estado,op1)
#           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# TypeError: evalSub3() missing 1 required positional argument: 'op1'
