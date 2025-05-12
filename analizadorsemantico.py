import pandas as pd
import analizadorsintactico as sintactico
import anytree as at
import numpy as np

#Cuerpo del Analizador Semantico
variables=[]

class estado:# es necesario agregar lexema?
# porque si se puede usar es necesario tener la raiz de parametro para: evaloperacion, asignarReal y asignarMatriz
  def __init__(self, id, tipo, valor, fila, columna):
    self.id = id
    self.tipo = tipo
    self.valor = valor
    self.fila = fila
    self.columna = columna
    
def evaloperacion(arbol,estado):
	if estado.tipo == 'real':
		asignarReal(arbol,estado):
	else:
		asignarMatriz(arbol,estado):
    
	
def asignarReal(arbol,estado):
	var = estado(arbol.lexema, arbol.complex,  int(arbol.name))
	if not(var in variables):
		variables.append(var)	 

def asignarMatriz(arbol, fila, columna):
  fila = trunc(fila)
  columna = trunc(columna)
  matriz = estado
  matriz.fila = fila
  matriz.columna = columna
  matriz.id = arbol.name
  matriz.tipo = 'Matriz'
  
  valor = []
  if fila == 1:
      while len(valor) < columna:
          valor.append(0)
      valor = np.array(valor)
  else:
      while len(valor) < fila:
          col = []
          while len(col) < columna:
              col.append(0)
          valor.append(col)
      valor = np.matrix(valor)
  matriz.valor = valor
  variables.append(matriz)
  

	
def obtenerVar(arbol,estado,tipo,fil,col):
  
  
  
#<Programa>::= 'Program' 'id' <EspacioVariables> <Cuerpo>
def evalPrograma(arbol,estado):
  evalEspacioVariables(arbol.children[2],estado) # arbol aca tendria que ser el puntero hijo de EspacioVariable
  evalCuerpo(arbol.children[3],estado)
#<EspacioVariables>::= 'id' '=' <Variable> <EV1>
def evalEspacioVariables(arbol,estado):
  evalVariable(arbol.children[2],estado,arbol.children[0].name) #puntero id nombre
  evalEV1(arbol.children[3],estado)
#<EV1>::= <EspacioVariables> |  epsilon
def evalEV1(arbol,estado):
  if arbol.name == 'epsilon':
    pass
  else:
    evalVariable(arbol.children[0],estado)
    
#<Variable>::= ‘TipoReal' | ‘[‘ ‘constanteReal’ ‘,’ ‘constanteReal’ ‘]’ 
def evalVariable(arbol,estado,nombre):
  if arbol=='Tiporeal':
    asignarVar(arbol,estado,arbol.children[0],0,0)
  elif arbol=='corcheteizq':
    asignarMatriz(arbol, arbol.children[1],arbol.children[3])
  
#<Cuerpo>:: '{'<Cuerpo2>’}’
def evalCuerpo(arbol,estado):
  evalCuerpo2(arbol.children[1],estado)
#<Cuerpo2>::= <Sentencia> <aux1>
def evalCuerpo2(arbol,estado):
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
  if arbol.name == 'asignacion':
    evalAsignacion(arbol.children[0],estado)
  elif arbol.name == 'lectura':
    evalLectura(arbol.children[0],estado)
  elif arbol.name == 'escritura':
    evalEscritura(arbol.children[0],estado)
  elif arbol.name == 'si':
    evalSi(arbol.children[0],estado)
  elif arbol.name == 'mientras':
    evalMientras(arbol.children[0],estado)
#<Lectura>::= 'peek’ ‘(' 'cadena' ',' 'id’ ’)'
def evalLectura(arbol,estado):
  valEscribir = input(arbol.children[0])
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
    val = evalExparit(arbol.children[0],estado)
  elif arbol.name == 'cadena':
    
#<Mientras>::= 'While ' <Condicion>':' <Cuerpo>
def evalMientras(arbol,estado):
  valor = evalCondicion(arbol.children[1],estado)
  while valor: 
    evalCuerpo(arbol.children[3],estado)
    valor = evalCondicion(arbol.children[1],estado)

  
  
  
#<Asignacion>::= 'id' <aux3>
def evalAsignacion(arbol,estado):
  evalAux3(arbol.children[1],estado)
#<aux3> ::=  '=' <ExpArit> | ‘[‘ <ExpArit> ‘,’ <ExpArit> ‘]’ ‘=’ <ExpArit>
def evalAux3(arbol,estado):
  if arbol.children[0].name == 'igual': #era igual o asignacion?
    evalExpArit(arbol.children[1],estado,res)
    asignarVar(variable,resultado)
  elif arbol.children[0].name == 'corcheteizq':
    evalExpArit(arbol.children[1],estado,fil)
    evalExpArit(arbol.children[3],estado,col)
    evalExpArit(arbol.children[5],estado,res)
#<ExpArit>::= <EAR1> <sub1> 
def evalExpArit(arbol,estado,res):
  evalEAR1(arbol.children[0],estado,res,op1) # en ves de eso, esto -->evalEAR1(arbol.children[0],estado,res) 
  evalSub1(arbol.children[1],estado,res,op1)
  # devolver un resultado de EAR
	# las EAR deben devolver un resultado
#<sub1>::= ‘+’ <ExpArit> | ‘-’ <ExpArit> | epsilon
def evalSub1(arbol,estado,res,op1):
  if arbol.children[0].name == 'suma':
    evalExpArit(arbol.children[1],estado,res,op2)
    op1 = op1 + op2
  elif arbol.children[0].name == 'menos':
    evalExpArit(arbol.children[1],estado,res,op2)
    op1 = op1 - op2
  elif arbol.children[0].name == 'epsilon':
    res = op1
#<EAR1>::= <EAR2> <sub2> 
def evalEAR1(arbol,estado):
  evalEAR2(arbol.children[0],estado,res,op1)
  evalSub2(arbol.children[1],estado,res,op1)
#<sub2>::= ‘*’ <EAR1> | ‘/’ <EAR1> | epsilon
def evalSub2(arbol,estado,res,op1):
  if arbol.children[0].name == 'multiplicacion':
    evalEAR1(arbol.children[1],estado,res,op2)
    op1 = op1 * op2
  elif arbol.children[0].name == 'division':
    evalEAR1(arbol.children[1],estado,res,op2)
    op1 = op1 / op2
  elif arbol.children[0].name == 'epsilon':
    res = op1
#<EAR2>::=  <EAR3> <sub3>
def evalEAR2(arbol,estado):
  evalEAR3(arbol.children[0],estado,res,op1)
  evalSub3(arbol.children[1],estado,res,op1)
#<sub3>::= ‘^’ <EAR2> | epsilon
def evalSub(arbol,estado,res,op1):
  if arbol.children[1].name == 'potencia'
    evalEar2(arbol.children[1],estado,res,op2)
    op1 = op1 ** op2
  elif arbol.children[0].name == 'epsilon':
    res = op1
#<EAR3>::= '('<ExpArit>')' |  'Transpose’ ‘(' <ExpArit> ')' | 'Size’ ‘(' <ExpArit> ',' 'constantereal' ')' | ‘id’ <EAR4> | ‘ConstanteReal’ | ‘-’<EAR3> | <constanteMatriz>
# EAR3 --> ‘ConstanteReal’ no se puede hacer o no se como?
def evalEAR3(arbol,estado,res,op1):
  if arbol.children[1].name =='exparit':
    evalExparit(arbol.children[1],estado)
  elif arbol.children[2].name == 'exparit':
    if arbol.children[2].name == 'coma':# si consideramos a las variables no hay que las distinga
      evalExparit(arbol.children[2],estado)
    else:
    	evalExparit(arbol.children[2],estado)
  elif arbol.children[1].name == 'ear4':
    evalEar4(arbol.children[1],estado)
  elif arbol.children[1].name == 'ear3':
    evalEar4(arbol.children[1],estado)
  elif arbol.children[1].name == 'constantematriz':
    evalconstanteMatriz(arbol.children[0],estado)
#<EAR4>::= ‘[‘ <ExpArit> ‘,’ <ExpArit> ‘]’ | epsilon 
def evalEAR4(arbol,estado):
  if arbol.children[0].name == 'epsilon':
    pass
  else:
    evalEar4(arbol.children[1],estado)
  
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
  evalCond1(arbol.children[0],estado)
  evalAux6(arbol.children[1],estado)
#<aux6>::= 'or' <Condicion> | epsilon
def evalAux6(arbol,estado):
  if arbol.children[0].name=='epsilon':
    pass
  else:
  	evalCondicion(arbol.children[1],estado)
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
    evalExparit(arbol.children[0],estado)
    evalExparit(arbol.children[2],estado)
  elif arbol.children[0].name=='llaveizq':
    evalCondicion(arbol.children[1],estado)

