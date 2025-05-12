f = open("algo.txt", "r")
cadena=f.read()
cadena=cadena.lstrip()
if cadena=='':
        print('fin')
for caracter in cadena:
    if caracter==None:
        print('fin')

f.close

