import os
import numpy as np
import analizadorsintactico as sintactico

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
    if estado[i].id == idEstado:
      return i
    else:
      i += 1
  raise Exception(f'No se definio la variable {idEstado}')

def analizadorSemantico(arbol):
  estado = []
  evalPrograma(arbol, estado)
  return estado

def asignarReal(estado,idVar):
  var = elemEstado(idVar, 'real', 0)
  estado.append(var)

def asignarMatriz(arbol, estado, nombre):
  fila = int(arbol.children[1].lexema)
  columna = int(arbol.children[3].lexema)
  if (fila <= 300 and fila >= 1) and (columna <= 300 and columna >= 1):
    valor = np.zeros((fila, columna))
    matriz = elemEstado(nombre, 'matriz', valor, fila, columna)
    estado.append(matriz)
  else:
     raise Exception('El tamaño maximo que una matriz puede tener es de 300 x 300')
  
def modificarVariableMatriz(estado, nombre, valor, fila, columna):
  i = recuperarEstado(nombre, estado)
  if (1 <= fila <= int(estado[i].fila)) and (1<= columna <= int(estado[i].columna)):
    estado[i].valor[(fila-1),(columna-1)] = valor

def modificarVariable(estado, nombre, valor):
  i = recuperarEstado(nombre, estado)
  estado[i].valor = valor
  
#<Programa>::= 'Program' 'id' <EspacioVariables> <Cuerpo>
def evalPrograma(arbol,estado):
  evalEspacioVariables(arbol.children[2],estado)
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
    asignarReal(estado,idVar)
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
  idtipo = arbol.children[4].lexema
  valEscribir = input((arbol.children[2].lexema)[1:-1])
  try:
    valEscribir = float(valEscribir)
  except:
    raise Exception('Se esperaba un real')
  i = recuperarEstado(idtipo, estado)
  estado[i].valor = valEscribir

#<Escritura>::= 'dump’ ‘(' <Lista> ')'
def evalEscritura(arbol,estado):
  print(evalLista(arbol.children[2],estado))
  
# <Lista>::= <VarLista><aux2>
def evalLista(arbol,estado):
  cadena=""
  parte = evalVarLista(arbol.children[0],estado)
  if isinstance(parte, np.ndarray):
    parte = '\n' + str(parte) + '\n'
  else:
    parte = str(parte)
  resto = str(evalAux2(arbol.children[1],estado))   
  if not(resto == 'None'):
    cadena = parte + resto
  else:
    cadena = parte
  return cadena

#<aux2> ::= ',' <Lista> | epsilon
def evalAux2(arbol,estado):
  if arbol.children[0].name=='epsilon':
    pass
  else:
    return evalLista(arbol.children[1],estado)
#<VarLista>::= 'cadena' | <ExpArit>  }
def evalVarLista(arbol,estado):
  if arbol.children[0].name == 'exparit':
    val = evalExpArit(arbol.children[0],estado)
    return val
  elif arbol.children[0].name == 'cadena':
    return (arbol.children[0].lexema)[1:-1]
    
#<Mientras>::= 'While ' <Condicion>':' <Cuerpo>
def evalMientras(arbol, estado):
    valor = evalCondicion(arbol.children[1], estado)
    while valor:
        evalCuerpo(arbol.children[3], estado)
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
  elif arbol.children[0].name == 'corcheteizq':
    fila = int(evalExpArit(arbol.children[1],estado))
    col = int(evalExpArit(arbol.children[3],estado))
    constanteReal = evalExpArit(arbol.children[6],estado)
    modificarVariableMatriz(estado,nombre,constanteReal, fila, col)

#<ExpArit>::= <EAR1> <sub1> 
def evalExpArit(arbol,estado):
  op1 = evalEAR1(arbol.children[0],estado) 
  res = evalSub1(arbol.children[1],estado,op1)
  return res
   
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
    pp = type(op1)
    if type(op1) is np.ndarray and type(op2) is np.ndarray:
      res = op2 @ op1
    else:
      res = op1 * op2
    return res
  elif arbol.children[0].name == 'dividir':
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

#<sub3>::= ‘^’ <EAR2> |epsilon
def evalSub3(arbol,estado,op1):
  if arbol.children[0].name == 'epsilon':
    return op1
  if arbol.children[0].name == 'potencia':
    print(arbol.children[1])
    if isinstance(op1, np.ndarray):
      if (op1.shape[0] == op1.shape[1]):
        print(arbol.children[1].lexema)
        op2 =int(evalEAR2(arbol.children[1],estado))
        if op2 >= 0:
          op1 = np.linalg.matrix_power(op1, op2)
          return op1 
        else:
          raise Exception('La potencia debe ser un numero positivo')
      else:
        raise Exception('La potencia solo se puede realizar con matrices cuadradas')
    else:
      op2 = float(evalEAR2(arbol.children[1],estado))
      op1 = op1 ** op2
      return op1
# def evalSub3(arbol,estado,op1):
#   if arbol.children[0].name == 'epsilon':
#     return op1
#   if type(op1) is not list:
#     op1 = float(op1)
#   if arbol.children[0].name == 'potencia':
#     op2 =float(evalEAR2(arbol.children[1],estado))
#     op1 = op1 ** op2
#     return op1
    
#<EAR3>::= '('<ExpArit>')' |  'Transpose’ ‘(' <ExpArit> ')' | 'Size’ ‘(' <ExpArit> ',' 'constantereal' ')' | ‘id’ <EAR4> | ‘ConstanteReal’ | ‘-’<EAR3> | <constanteMatriz>
def evalEAR3(arbol,estado):
  if arbol.children[0].name == 'constantereal':
    return float(arbol.children[0].lexema)
  elif arbol.children[0].name == 'constantematriz':
    return evalconstanteMatriz(arbol.children[0],estado)
  elif arbol.children[0].name == 'size':
    matriz = evalExpArit(arbol.children[2],estado)
    fila, columna = matriz.shape
    if arbol.children[4].lexema == '1': # es fila
      return fila
    elif arbol.children[4].lexema == '2': # es columna
      return columna
    else:
      raise Exception('1: fila, 2: columna, para el size')
  elif arbol.children[0].name == 'transpose':
    matrizT = evalExpArit(arbol.children[2],estado)
    return matrizT.T
  if arbol.children[0].name =='parentesisizq':
    return evalExpArit(arbol.children[1],estado)
  elif arbol.children[0].name == 'id':
    return evalEAR4(arbol.children[1],estado,arbol.children[0].lexema)
  elif arbol.children[0].name == 'menos':
    return evalEAR3(arbol.children[1],estado)

#<EAR4>::= ‘[‘ <ExpArit> ‘,’ <ExpArit> ‘]’ | epsilon 
def evalEAR4(arbol,estado,id):
  if arbol.children[0].name == 'epsilon':
    indice = recuperarEstado(id, estado)
    return estado[indice].valor
  else:
    ind = recuperarEstado(id, estado)
    matriz = estado[ind].valor
    subFila = int(evalExpArit(arbol.children[1],estado))
    subCol = int(evalExpArit(arbol.children[3],estado))
    return matriz[subFila-1][subCol-1]

#<constanteMatriz>::= ‘[‘ <Filas> ‘]’ 
def evalconstanteMatriz(arbol,estado):
  matriz=[]
  evalFilas(arbol.children[1],estado,matriz)
  mLexema = np.vectorize(matrizLexema)
  matriz = mLexema(matriz)
  return matriz

# esta funcion devuelve la matriz de lexemas de un elemento
def matrizLexema(elemento):
  return float(elemento.lexema)

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
  bool = evalCondicion(arbol.children[1],estado)
  if bool:
    evalCuerpo(arbol.children[3],estado)
  else:
    evalSii(arbol.children[4],estado)

#<Sii>::= 'else' ’:’ <Cuerpo> | 'elif' <Condicion> ':' <Cuerpo> <Sii> | epsilon
def evalSii(arbol,estado):
  if arbol.children[0].name=='else':
    evalCuerpo(arbol.children[2],estado)
  elif arbol.children[0].name=='elif':
    bool1 = evalCondicion(arbol.children[1],estado)
    if bool1:
      evalCuerpo(arbol.children[3],estado)
    else:
      evalSii(arbol.children[4],estado)
  elif arbol.children[0].name=='epsilon':
    pass

#<Condicion>::= <COND1> <aux6> 
def evalCondicion(arbol,estado):
  val = evalCond1(arbol.children[0],estado)
  res = evalAux6(arbol.children[1], estado, val)
  return res

#<aux6>::= 'or' <Condicion> | epsilon
def evalAux6(arbol, estado, cond1):
  if arbol.children[0].name=='epsilon':
    return cond1
  else:
    cond2 = evalCondicion(arbol.children[1], estado)
    return (cond1 or cond2)
  
#<COND1>::= <COND2> <aux7> 
def evalCond1(arbol,estado):
  val = evalCond2(arbol.children[0],estado)
  res = evalAux7(arbol.children[1], estado, val)
  return res

#<aux7>::= 'and' <COND1> | epsilon
def evalAux7(arbol, estado, cond1):
  if arbol.children[0].name=='epsilon':
    return cond1
  else:
    cond2 = evalCond1(arbol.children[1], estado)
    return (cond1 and cond2)

#<COND2>::= ‘not’ <COND2> | <ExpArit> ‘opRelacional’ <ExpArit> | ‘{‘ <Condicion> ‘}’
def evalCond2(arbol,estado):
  if arbol.children[0].name=='not':
    return not(evalCond2(arbol.children[1],estado))
  elif arbol.children[0].name=='exparit':
    exp1 = evalExpArit(arbol.children[0],estado)
    exp2 = evalExpArit(arbol.children[2],estado)
    operador = arbol.children[1].lexema
    operador=operador.lstrip()
    if operador == '==':
      return (exp1 == exp2)
    elif operador == '>':
      return (exp1 > exp2)
    elif operador == '<':
      return (exp1 < exp2)
    elif operador == '>=':
      return (exp1 >= exp2)
    elif operador == '<=':
      return (exp1 <= exp2)
    elif operador == '!=':
      return (exp1 != exp2)
  elif arbol.children[0].name=='llaveizq':
    return evalCondicion(arbol.children[1],estado)
  else:
    raise Exception('Condicion no valida')

if __name__ == "__main__":
  script_dir = os.path.dirname(__file__)
  file_path = os.path.join(script_dir, 'Codigo.txt')
  texto = open(file_path).read()
  arbol, ccomplex = sintactico.analizadorSintactico(texto)
  analizadorSemantico(arbol)
#  if arbol:
#    est = analizadorSemantico(arbol)
#    for elemento in est:
#      print(f'nombre = {elemento.id}')
#      print(f'valor = {elemento.valor}')