import os
import pandas as pd
import analizadorlexico as lexico
import anytree as at

variables = ['programa','espaciovariables','ev1',
    'variable','cuerpo','cuerpo2','aux1','sentencia','lectura','escritura','lista','aux2','varlista',
    'mientras','asignacion','aux3','exparit','sub1','ear1','sub2','ear2','sub3','ear3','filas','aux4',
    'listanumeros','aux5','si','sii','condicion','aux6','cond1','aux7','cond2','constantematriz','ear4']

terminales = ['program','id','asignar','tiporeal','corcheteizq','corcheteder','constantereal','coma',
    'llaveizq','llaveder','peek','dump','if','while','else','elif','not','or','dospuntos','parentesisizq',
    'parentesisder','transpose','size','menos','and','potencia','dividir','multiplicacion','suma','igual','cadena','oprelacional']
def analizadorSintactico(texto):
    poss = 0
    script_dir = os.path.dirname(__file__)
    csv_path = os.path.join(script_dir, 'TAS-Minus.csv')
    df = pd.read_csv(csv_path) #Por si no arranca
    df.set_index('Unnamed: 0', inplace=True)
    pesos = at.Node('pesos') # pesos del arbol es programa
    programa = at.Node('programa')
    pila = [pesos, programa]
    texto, ccomplex, poss, llexema = lexico.sigCompLex(texto, poss)
    while (ccomplex != 'pesos') and (ccomplex != 'error'):
        nodoPila = pila.pop()
        nombreNodo = nodoPila.name
        if nombreNodo in variables:
            fila = nombreNodo
            columna = ccomplex[1:]
            celdaTAS = df.loc[fila, columna]
            if pd.isna(celdaTAS):
                ccomplex = 'error'
                print(f"Error: No se encontró la celda para {fila} y {columna}")

            else:
                cTas=str(celdaTAS).split()
                tam = len(cTas) - 1
                for i in range(len(cTas)):
                    aux = cTas[i]
                    naux = at.Node(aux, parent=nodoPila)
                for j in range(len(cTas)):
                    pila.append(nodoPila.children[tam-j])      
        elif nombreNodo in terminales:            
            if nombreNodo == ccomplex[1:]:
                nodoPila.lexema = llexema       # Guardamos el lexema general
                nodoPila.complex = ccomplex     # Guardamos la categoría gramatical
                texto, ccomplex, poss, llexema = lexico.sigCompLex(texto, poss)
            else:
                ccomplex = 'error'
                
        elif nombreNodo == 'epsilon':
            pass
        else:
            ccomplex = 'error'
            
    nodoPila = pila.pop()
    nombreNodo = nodoPila.name
    return  programa, ccomplex


if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, 'Codigo.txt')
    texto = open(file_path).read()
    texto = texto.lower()
    arbol, ccomplex= analizadorSintactico(texto)
    if ccomplex == 'error':
        print('ccomplex = error')
    if arbol:
        with open("arbol.txt", "w", encoding="utf-8") as f:
            for pre, fill, node in at.RenderTree(arbol, style=at.ContStyle):
                lex = getattr(node, 'lexema', '')
                if lex == '':
                    f.write(f"{pre}{node.name}\n")
                else:
                    f.write(f"{pre}{node.name} lexema: {lex}\n")
        print("Árbol guardado en arbol.txt")
    else:
        print("El árbol no se ha construido correctamente.")