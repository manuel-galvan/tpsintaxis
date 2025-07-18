![rd logo](https://github.com/user-attachments/assets/ce517ca6-f81b-4f12-9735-5bb56c306b42)
<h1>rd es un lenguaje escrito en python que trabaja sobre matrices y reales</h1>
<br>
<h2>Que significa rd</h2>
<p>rd viene de un juego de palabras con el apellido de John McCarthy, padre de la Inteligencia Artificial y del lenguaje LISP</p>
<br>
<h2>Documentacion</h2>
<ul>
  <li><a href='sintaxis-basica'>Sintaxis basica</a></li>
  <li><a href='#lectura'>Lectura</a></li>
  <li><a href='#escritura'>Escritura</a></li>
  <li><a href='#ejemplos-de-codigo'>Ejemplos de codigo</a></li>
</ul>

### Sintaxis basica
```
Program nombrePrograma
variableReal = real
variableMatriz = [2,2]
{
//Cuerpo del programa
}
```

### Lectura
La lectura se hace con el comando `peek`. El comando peek acepta dos parametros, primero una cadena que sera mostrada por pantalla y la variable en la que se escribira la lectura.
```
peek('cadena', variable)
```
Al ser rd un lenguaje que solo trabaja con escalares, al intentar escribir sobre una variable solo se acepta un escalar, intentar escribir un caracter que no sea un digito resultara en un error.
<br>

### Escritura

La escritura por pantalla se hace con el comando `peek`. El comando dump acepta una lista de cadenas o variables separadas por coma.

```
dump('una cadena', unNumero)
```

### Ejemplos de codigo

> Sumas, restas, divisiones, potencias y raices.

```
Program OperacionesAritmeticasReales
  num = real
  num1 = real
  num2 = real
  num3 = real
  suma = real
  resta = real
  division = real
  multiplicacion = real
  potencia = real
  raiz = real
{
  num = 2
  num1 = 3
  num2 = 4
  num3 = 5
  suma = num + num1
  resta = num2 - num3
  division = num3 / num
  multiplicacion = num1 * num2
  potencia = num ^ num2
  raiz = num2 ^ (1/num)
  dump(suma)
  dump(resta)
  dump(division)
  dump(multiplicacion)
  dump(potencia)
  dump(raiz)
}
```
> Utilizacion de matrices y operaciones entre matrices

```
Program OperacionesAritmeticasMatriciales
  matriz = [2,2]
  matriz1 = [2,2]
  sumaM = [2,2]
  restaM = [2,2]
  multiplicacionM = [2,2]
  productoPorEscalarM = [2,2]
  matrizT = [2,2]
  escalar = real
  tam = real
{
  escalar = 2
  matriz = [[1,2],[3,4]]
  matriz1 = [[5,6],[7,8]]
  sumaM = matriz + matriz1
  restaM = matriz1 - matriz
  multiplicacionM = matriz1 * matriz
  productoPorEscalarM = matriz * escalar
  tam = size(matriz,2)
  matrizT = transpose(matriz)
  dump(sumaM)
  dump(restaM)
  dump(multiplicacionM)
  dump(productoPorEscalarM)
  dump(tam)
  dump(matrizT)
}

```
