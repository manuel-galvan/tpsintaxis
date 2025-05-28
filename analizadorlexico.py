import string
opcon=['\x00', '\x01', '\x02', '\x03', '\x04', '\x05', '\x06', '\x07', '\x08', '\t', '\n', '\x0b', '\x0c', '\r', '\x0e', '\x0f', '\x10', '\x11', '\x12', '\x13', '\x14', '\x15', '\x16', '\x17', '\x18', '\x19', '\x1a', '\x1b', '\x1c', '\x1d', '\x1e', '\x1f']
#TSG
#Revisar que se llamen a todos los terminales, que tengan los mismos nombres en AL en AS y en la TAS.
TipoSimboloGramatical=['Vprograma', 'Vespvar', 'Vespvar1', 'Vvar', 'Vcuerpo', 'Vcuerpo2', 'Vaux1', 'Vsentencia', 'Vlectura', 'Vescritura',
    'Vlista', 'Vaux2', 'Vvarlista', 'Vmientras', 'Vasignacion', 'Vaux3', 'Vexparit', 'Vsub1', 'Vear1', 'Vsub2', 'Vear2',
    'Vsub3', 'Vear3', 'Vear4', 'Vconstmatriz', 'Vfilas', 'Vaux4', 'Vlistanum', 'Vaux5', 'Vsi', 'Vsii', 'Vcond', 'Vaux6',
    'Vcond1', 'Vaux7', 'Vcond2','Tprogram', 'Tid', 'Tasignacion', 'Ttiporeal', 'Tconstreal', 'Tcadena', 'Toprel', 'Tllaveizq', 'Tllaveder', 'Tcorcheteizq',
    'Tcorcheteder', 'Tcoma', 'Tparentesisizq', 'Tparentesisder', 'Tdospuntos', 'Tsuma', 'Tresta', 'Tmultiplicacion',
    'Tdivision', 'Tpotencia', 'Tprogram', 'Tpeek', 'Tdump', 'Tif', 'Twhile', 'Telif', 'Telse', 'Tnot', 'Tor', 'Ttranspose',
    'Tsize', 'Tand', 'pesos', 'error']

def CarASimb(car):
    num=('0','1','2','3','4','5','6','7','8','9')
    match car:
        case car if car in tuple(string.ascii_lowercase) or car in tuple(string.ascii_uppercase):
            return 0
        case car if car in num:
            return 1
        case '-':
            return 2
        case '"':
            return 3
        case ',':
            return 4
        case '_':
            return 5
        case _:
            return 6

def CarASimb1(car): # Version de Caracter a Simbolo para esReal
    num=('0','1','2','3','4','5','6','7','8','9')
    match car:
        case car if car in tuple(string.ascii_lowercase) or car in tuple(string.ascii_uppercase):
            return 0
        case car if car in num:
            return 1
        case '-':
            return 2
        case '"':
            return 3
        case '.':
            return 4
        case '_':
            return 5
        case _:
            return 6
#0 es una letra, 1 es un digito, 2  es guion, 3 es comilla, 4 es punto, 
#5 es guion bajo, 6 es otro
        
def esPalabraReservada(fuente):
  
  if (len(fuente) >= 7) and (fuente[:7]=='program'):
    return(True,'Tprogram',7)
  if (len(fuente) >= 4) and (fuente[:4]=='peek'):
    return(True,'Tpeek',4)
  if (len(fuente) >= 4) and (fuente[:4]=='dump'):
    return(True,'Tdump',4)
  if (len(fuente) >= 2) and (fuente[:2]=='if'):
    return(True,'Tif',2)
  if (len(fuente) >= 5) and (fuente[:5]=='while'):
    return(True,'Twhile',5)
  if (len(fuente) >= 4) and (fuente[:4]=='elif'):
    return(True,'Telif',4)
  if (len(fuente) >= 4) and (fuente[:4]=='else'):
    return(True,'Telse',4)
  if (len(fuente) >= 3) and (fuente[:3]=='not'):
    return(True,'Tnot',3)
  if (len(fuente) >= 2) and (fuente[:2]=='or'):
    return(True,'Tor',2)
  if (len(fuente) >= 9) and (fuente[:9]=='transpose'):
    return(True,'Ttranspose',9)
  if (len(fuente) >= 4) and (fuente[:4]=='size'):
    return(True,'Tsize',4)
  if (len(fuente) >= 3) and (fuente[:3]=='and'):
    return(True,'Tand',3)
  if (len(fuente) >= 4) and (fuente[:4]=='real'):
    return(True,'Ttiporeal',4)
  else:
      return(False,'',0)


def esIdentificador(cadena):
    posicion=0
    F=[3]
    EstadoActual=0
    Delta=[
     [1,2,2,2,2,2,2],
     [1,1,1,2,2,1,3],
     [2,2,2,2,2,2,2],
     [3,3,3,3,3,3,3]
    ]
    while EstadoActual not in (3,2):
        EstadoActual=Delta[EstadoActual][CarASimb(cadena[posicion])]
        posicion+=1
    if EstadoActual in F:
        return (True, 'Tid', posicion-1)
    else:
        return (False,'',0)
def esCadena(cadena):
    lexema=''
    F=[5]
    posicion=0
    EstadoActual=0
    Delta=[
     [4,4,4,1,4,4,4],
     [2,2,2,3,2,2,2],
     [2,2,2,3,2,2,2],
     [4,4,4,4,5,4,5],
     [4,4,4,4,4,4,4],
     [5,5,5,5,5,5,5]
    ]
    while EstadoActual not in (4,5):
        EstadoActual=Delta[EstadoActual][CarASimb(cadena[posicion])]
        posicion+=1
        if posicion < len(cadena):
            lexema=lexema + cadena[posicion]
    if EstadoActual in F:
        return (True, 'Tcadena', posicion-1)
    else:
        return (False,'',0)
    
def esReal(cadena):
    F=[4]
    EstadoActual=0
    posicion=0
    Delta=[[5,2,1,5,5,5,5],
           [5,1,5,5,5,5,5],
           [4,2,4,4,3,4,4],
           [5,6,5,5,5,5,5],
           [4,4,4,4,4,4,4],
           [5,5,5,5,5,5,5],
           [4,6,4,4,4,4,4]
           ]
    while EstadoActual not in (4,5):
        EstadoActual=Delta[EstadoActual][CarASimb1(cadena[posicion])]
        posicion +=1
    if EstadoActual in F:
        return (True, 'Tconstantereal', posicion-1)
    else:
        return (False,'',0)

def esSimbolo(fuente): #Toprel, Tllaveizq, Tllaveder, Tcorcheteizq, Tcorcheteder, Tcoma, Tparentesisizq, Tparentesisder, Tdospuntos, Tsuma, Tresta, Tmultiplicacion, Tdivision, Tpotencia,
    car = fuente[0]
    if car == '{':
        return (True, 'Tllaveizq',1)
    elif car == '}':
        return (True, 'Tllaveder',1)
    elif car == '[':
        return (True, 'Tcorcheteizq',1)
    elif car == ']':
        return (True, 'Tcorcheteder',1)
    elif car == ',':
        return (True, 'Tcoma',1)
    elif car == '(':
        return (True, 'Tparentesisizq',1)
    elif car == ')':
        return (True, 'Tparentesisder',1)
    elif car == ':':
        return (True, 'Tdospuntos',1)
    elif car == '+':
        return (True, 'Tsuma',1)
    elif car == '-':
        return (True, 'Tmenos',1)
    elif car == '*':
        return (True, 'Tmultiplicacion',1)
    elif car == '/':
        return (True, 'Tdividir',1)
    elif car == '^':
        return (True, 'Tpotencia',1)
    elif car == '=':
        if fuente[1] == '=' or fuente[1] == '<' or fuente[1] == '>': #agregar todos los operadores relacionales. Toprel           
            return(True,'Toprelacional',2)
        else:
            return (True, 'Tasignar',1)
    elif car == '<' or car == '>':
       return(True,'Toprelacional',2)
    else:
        return(False,'',0)
        
def sigCompLex(fuente,pos):
    #Inicializar
    opcon=[]
    i=1
    car=''
    posicion=0
    #Eliminar lexema anterior
    fuente =fuente[pos:].lstrip()
    
     #Saltar
    """"for i in range(32):
        opcon.append(chr(i))"""
    while fuente[:posicion] in opcon:
        posicion+=1
        fuente=fuente[posicion:].lstrip()
    # FUNCIONES """ES"""

    if fuente == '':
        complex='pesos'
        lexema=''
        
    elif esPalabraReservada(fuente)[0]:
      complex= esPalabraReservada(fuente)[1]
      pos= esPalabraReservada(fuente)[2]
    #Consultar si está bien hecho agregando con append al TSG   
    elif esIdentificador(fuente)[0]:
      complex= esIdentificador(fuente)[1]
      pos= esIdentificador(fuente)[2]
      lexema='T'+fuente[:pos]
      if not(lexema in TipoSimboloGramatical):
          TipoSimboloGramatical.append(lexema) # TSagregar 
      
    elif esCadena(fuente)[0]:
      complex= esCadena(fuente)[1]
      pos= esCadena(fuente)[2]
        
    elif esReal(fuente)[0]:
      complex= esReal(fuente)[1]
      pos= esReal(fuente)[2]
        
    elif esSimbolo(fuente)[0]:
       complex= esSimbolo(fuente)[1]
       pos= esSimbolo(fuente)[2]
    else: 
       complex= 'error'
       pos=0
  
    lexema=fuente[:pos]
    return(fuente,complex,pos,lexema)
  
# Codigo.txt
'''Program julian    
num1 = real
num2 = real

{if num1 ==num2:
{num1=num2+1}}'''
    
# <<<<<<<<<--------- Prueba
if __name__ == "__main__":
    ccomplex=''
    poss=0
    import os
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, 'Codigo.txt')
    texto = open(file_path).read()
    #
    j=0
    print(texto,'\n')
    while not(ccomplex == 'pesos') and not(ccomplex == 'error'): #Tllaveder es como pesos
        texto, ccomplex, poss, llexema= sigCompLex(texto,poss)
        print('\n\n')
        
        print('complex: ',ccomplex,'lexema: ',llexema)
        if (ccomplex == 'Tllaveder'):
            pass
        else:
            #print('texto[',poss,']: ',texto[poss])
            print('\n\n')
    print(TipoSimboloGramatical)