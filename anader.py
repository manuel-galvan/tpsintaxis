archivo='TAS.csv'


TAS= open(archivo).read()
pal=''
char=''

i=0
#i posicion actual
ListaTAS=[]
FilaTAS=[]
while i < len(TAS): # Crea una Matriz de la TAS
    if TAS[i] == chr(10):
        n=0
        FilaTAS.append(pal)
        pal=''
        ListaTAS.append(FilaTAS)
        FilaTAS=[]
        i+=1
    elif TAS[i] == ',':
        FilaTAS.append(pal)
        pal=''
        i+=1
    else:
        pal+= TAS[i]
        i+=1

print(ListaTAS)