import string

def CarASimb(car):
    num=('0','1','2','3','4','5','6','7','8','9')
    match car:
        case car if car in tuple(string.ascii_lowercase) or car in tuple(string.ascii_uppercase):
            return 0
        case car if car in num:
            return 1
        case '-':
            return 2

def esIdentificador(cadena):
    F=[1]
    EstadoActual=0
    Delta=[
     [1,2,2],
     [1,1,1],
     [2,2,2],
     [1,1,2],
    ]
    for caracter in range(len(cadena)):
        EstadoActual=Delta[EstadoActual][CarASimb(cadena[caracter])]
    if EstadoActual in F:
        return True
    else:
        return False



nom=input ('Cadena: ')
val=esIdentificador(nom)
if val==True:
    print('Valido')
else:
    print('Invalido')
input()
