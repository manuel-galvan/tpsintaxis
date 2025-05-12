import string

import string
cadena=''
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
        case '.':
            return 4
        case '_':
            return 5
        case _:
            return 6

def esReal(cadena):
    F=[2,5]
    EstadoActual=0
    Delta=[
     [4,2,1,4,3,4,4],
     [4,2,4,4,3,4,4],
     [4,2,4,4,3,4,4],
     [4,2,4,4,4,4,4],
     [4,4,4,4,4,4,4],
     [4,5,4,4,4,4,4]
    ]
    for caracter in range(len(cadena)):
        EstadoActual=Delta[EstadoActual][CarASimb(cadena[caracter])]
    if EstadoActual in F:
        return True
    else:
        return False



nom=input ('Cadena: ')
val=esReal(nom)
if val==True:
    print('Valido')
else:
    print('Invalido')
input()
