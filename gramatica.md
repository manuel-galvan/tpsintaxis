<Programa>::= 'Program' 'id' <EspacioVariables> <Cuerpo>
<EspacioVariables>::= 'id' '=' <Variable> <EV1>
<EV1>::= <EspacioVariable> |  epsilon
<Variable>::= ‘TipoReal' | ‘[‘ ‘constanteReal’ ‘,’ ‘constanteReal’ ‘]’ 
<Cuerpo>:: '{'<Cuerpo2>’}’
<Cuerpo2>::= <Sentencia> <aux1>
<aux1>::= <Cuerpo2> | epsilon 
<Sentencia>::= <Asignacion> | <Lectura> | <Escritura> | <Si> | <Mientras>
<Lectura>::= 'peek’ ‘(' 'cadena' ',' 'id’ ’)'
<Escritura>::= 'dump’ ‘(' <Lista> ')'
<Lista>::= <VarLista><aux2>
<aux2> ::= ',' <Lista> | epsilon
<VarLista>::= 'cadena' | <ExpArit>                       
<Mientras>::= 'While ' <Condicion>':' <Cuerpo>
<Asignacion>::= 'id' <aux3>
<aux3> ::=  '=' <ExpArit> | ‘[‘ <ExpArit> ‘,’ <ExpArit> ‘]’ ‘=’ <ExpArit>
<ExpArit>::= <EAR1> <sub1> 
<sub1>::= ‘+’ <ExpArit | ‘-’ <ExpArit> | epsilon
<EAR1>::= <EAR2> <sub2> 
<sub2>::= ‘*’ <EAR1> | ‘/’ <EAR1> | epsilon
<EAR2>::=  <EAR3> <sub3> 
<sub3>::= ‘^’ <EAR2> | epsilon
<EAR3>::= '('<ExpArit>')' |  'Transpose’ ‘(' <ExpArit> ')' | 'Size’ ‘(' <ExpArit> ',' 'entero' ')' | <EAR4> | ‘ConstanteReal’ | ‘-’<EAR3> | <constanteMatriz>
<EAR4>::= ‘[‘ <ExpArit> ‘,’ <ExpArit> ‘]’ | epsilon
<constanteMatriz>::= ‘[‘ <Filas> ‘]’            
<Filas>::=  ‘[‘<listaNumeros>’]’ <aux4>
<aux4>::= ‘,’ <Filas> | epsilon
<listaNumeros>::= ‘ConstanteReal’ <aux5> 
<aux5>::= ‘,’ <listaNumeros> | epsilon
<Si>::= 'If ' <Condicion> ':' <Cuerpo> <Sii>
<Sii>::= 'else:' <Cuerpo> | 'elif' <Condicion> ':' <Cuerpo> <Sii> | epsilon
<Condicion>::= <COND1> <aux6> 
<aux6>::= 'or' <Condicion> | epsilon
<COND1>::= <COND2> <aux7> 
<aux7>::= 'and' <COND1> | epsilon
<COND2>::= ‘not’ <COND2> | <ExpArit> ‘opRelacional’ <ExpArit> | ‘{‘ <Condicion> ‘}’
