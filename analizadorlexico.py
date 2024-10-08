import string
vcomplex,vlex,cadena,lexema='','','',''
vbool=False
textolista=[]
complexlista=[]
#TSG
TipoSimboloGramatical=(
    #Variables
    'Vprograma', 'Vespvar', 'Vespvar1', 'Vvar', 'Vcuerpo', 'Vcuerpo2', 'Vaux1', 'Vsentencia', 'Vlectura', 'Vescritura',
    'Vlista', 'Vaux2', 'Vvarlista', 'Vmientras', 'Vasignacion', 'Vaux3', 'Vexparit', 'Vsub1', 'Vear1', 'Vsub2', 'Vear2',
    'Vsub3', 'Vear3', 'Vear4', 'Vconstmatriz', 'Vfilas', 'Vaux4', 'Vlistanum', 'Vaux5', 'Vsi', 'Vsii', 'Vcond', 'Vaux6',
    'Vcond1', 'Vaux7', 'Vcond2',
    #Terminales -----> Tasignacion = Toprel????
    'Tprogram', 'Tid', 'Tasignacion', 'Treal', 'Tconstreal', 'Tcadena', 'Toprel', 'Tllaveizq', 'Tllaveder', 'Tcorcheteizq',
    'Tcorcheteder', 'Tcoma', 'Tparentesisizq', 'Tparentesisder', 'Tdospuntos', 'Tsuma', 'Tresta', 'Tmultiplicacion',
    'Tdivision', 'Tpotencia', 'Tprogram', 'Tpeek', 'Tdump', 'Tif', 'Twhile', 'Telif', 'Telse', 'Tnot', 'Tor', 'Ttranspose',
    'Tsize', 'Tand', 'pesos', 'error')

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

#0 es una letra, 1 es un digito, 2  es guion, 3 es comilla, 4 es punto, 
#5 es guion bajo, 6 es otro
        
def esPalabraReservada(cadena):
    complex=''
    palabras=['Program','peek','dump','if','While','elif','else','not','or','Transpose''size','and','real'] #12 subrango de TSG
    if cadena in palabras:
        complex='T' + cadena.lower()
        return (True, complex)
    else:
        return(False,'')


def esIdentificador(cadena):
    F=[1]
    EstadoActual=0
    Delta=[
     [1,2,2,2,2,2,2],
     [1,1,1,2,2,1,2],
     [2,2,2,3,2,2,2]
    ]
    for caracter in range(len(cadena)):        
        EstadoActual=Delta[EstadoActual][CarASimb(cadena[caracter])]
    if EstadoActual in F:
        return (True, 'Tid', lexema)
    else:
        return (False,'',lexema)
def esCadena(cadena):
    lexema=''
    F=[3]
    EstadoActual=0
    Delta=[
     [4,4,4,1,4,4,4],
     [2,2,2,3,2,2,2],
     [2,2,2,3,2,2,2],
     [4,4,4,4,4,4,4],
     [4,4,4,4,4,4,4]
    ]
    for caracter in range(len(cadena)):        
        EstadoActual=Delta[EstadoActual][CarASimb(cadena[caracter])]
        lexema=lexema + cadena[caracter]
    if EstadoActual in F:
        return (True, 'Tcadena', lexema)
    else:
        return (False,'',lexema)
    
def esReal(cadena):
    F=[2,3]
    EstadoActual=0
    Delta=[
     [4,2,1,4,4,4,4],
     [4,2,4,4,4,4,4],
     [4,2,4,4,3,4,4],
     [4,3,4,4,4,4,4],
     [4,4,4,4,4,4,4]
    ]
    for caracter in range(len(cadena)):
        EstadoActual=Delta[EstadoActual][CarASimb(cadena[caracter])]
    if EstadoActual in F:
        return (True, 'Treal')
    else:
        return (False,'')

def esSimbolo(car): #Toprel, Tllaveizq, Tllaveder, Tcorcheteizq, Tcorcheteder, Tcoma, Tparentesisizq, Tparentesisder, Tdospuntos, Tsuma, Tresta, Tmultiplicacion, Tdivision, Tpotencia,
    if car == '{':
        return (True, 'Tllaveizq')
    elif car == '}':
        return (True, 'Tllaveder')
    elif car == '[':
        return (True, 'Tcorcheteizq')
    elif car == ']':
        return (True, 'Tcorcheteder')
    elif car == ',':
        return (True, 'Tcoma')
    elif car == '(':
        return (True, 'Tparentesisizq')
    elif car == ')':
        return (True, 'Tparentesisder')
    elif car == ':':
        return (True, 'Tdospuntos')
    elif car == '+':
        return (True, 'Tsuma')
    elif car == '-':
        return (True, 'Tresta')
    elif car == '*':
        return (True, 'Tmultiplicacion')
    elif car == '/':
        return (True, 'Tdivision')
    elif car == '^':
        return (True, 'Tpotencia')
    elif car == '=':
        return (True, 'Tasignacion')
    else:
        return(False,'')
        
def textoaLista(texto):    
    pal=''
    for car in texto:
        if car=='=':
            textolista.append(pal)
            textolista.append('=')
            pal=''
        elif car=='+':
            textolista.append(pal)
            textolista.append('+')
            pal=''
        elif car=='-':
            textolista.append(pal)
            textolista.append('-')
            pal=''
        elif car=='*':
            textolista.append(pal)
            textolista.append('*')
            pal=''
        elif car=='/':
            textolista.append(pal)
            textolista.append('/')
            pal=''
        elif car=='^':
            textolista.append(pal)
            textolista.append('^')
            pal=''
        elif car=='(':
            textolista.append(pal)
            textolista.append('(')
            pal=''
        elif car==')':
            textolista.append(pal)
            textolista.append(')')
            pal=''
        elif car=='{':
            textolista.append(pal)
            textolista.append('{')
            pal=''
        elif car=='}':
            textolista.append(pal)
            textolista.append('}')
            pal=''
        elif car=='[':
            textolista.append(pal)
            textolista.append('[')
            pal=''
        elif car==']':
            textolista.append(pal)
            textolista.append(']')
            pal=''
        elif car==':':
            textolista.append(pal)
            textolista.append(':')
            pal=''
        elif car == ' ' or car == '\n':
            textolista.append(pal)
            pal=''
        else:
            pal= pal + car
    while '' in textolista:
        textolista.remove('')
        
def listaalista(textolista):
    for lex in textolista:
        if esPalabraReservada(lex)[0]:
            complexlista.append(esPalabraReservada(lex)[1])
            
        elif esIdentificador(lex)[0]:
            complexlista.append(esIdentificador(lex)[1])
            
        elif esCadena(lex)[0]:
            complexlista.append(esCadena(lex)[1])
            
        elif esReal(lex)[0]:
           complexlista.append(esReal(lex)[1])
            
        elif esSimbolo(lex)[0]:
            complexlista.append(esSimbolo(lex)[1])
            
        elif esPalabraReservada(lex)[0]:
            complexlista.append(esPalabraReservada(lex)[1])
            
if __name__ == "__main__":


    texto=open('Codigo.txt').read()
    texto= texto+' '
    textoaLista(texto)
    listaalista(textolista)
    for i in range(len(textolista)):
        print(textolista[i],' : ',complexlista[i])

    '''
    vbool,vcomplex,vlex=esCadena(texto)
    print('bool: ',vbool,'Componente Lexico: ',vcomplex,'Lexema: ',vlex)
    '''
