from numpy import array


def ingresarRestricciones(cantRestricciones,cantVariables):
    arrayFO = []
    for i in range(cantVariables):
        datoFO = float(input(f"Digite valor funcion objetivo X{i}: "))
        arrayFO.append(datoFO)

    arrayRestricciones = []

    for i in range(cantRestricciones):
        arrayAux = []
        for j in range(cantVariables):
            datoRestricciones = float(input(f"Digite valor Restriccion {i} para la variable X{j}: "))
            arrayAux.append(datoRestricciones)

        signoRestriccion = int(input("Digite el signo >=:1  <=:2  =:3 "))
        valorRestriccion = float(input("Digite el valor de la restriccion: "))

        arrayAux.append(signoRestriccion)
        arrayAux.append(valorRestriccion)
        arrayRestricciones.append(arrayAux)
    
    return arrayFO, arrayRestricciones


# Se genenran los arreglos en 0 segun el tipo
# Tipo = 1 => Filas y columnas
# Tipo = 2 => Filas
# Tipo = 3 => Columnas
def crearMatrizCeros(filas,columnas,tipo):
    array = []
    # Matriz de ceros
    if(tipo == 1):
        for i in range(filas):
            arrayAux = []
            for j in range(columnas):
                arrayAux.append(0)
            array.append(arrayAux)

    elif(tipo == 2):
        for i in range(filas):
            array.append(0)
    elif(tipo == 3):
        for i in range(columnas):
            array.append(0)

    return array

def definirMatriz(arrayRestricciones, variables, restricciones):
    cantColumnas= 0
    cantFilas = 0
    cantVariablesArtificiales = 0
    arrayNormalizado = []
    arrayFinal = []
    # Obteniendo filas y columnasvariables
    cantFilas = restricciones

    for i in range(len(arrayRestricciones)):
        #Obtenemos el signo
        if arrayRestricciones[i][variables] == 1:
            cantVariablesArtificiales+=1
    cantColumnas = restricciones + cantVariablesArtificiales

    #arrayNormalizado = crearMatrizCeros(cantFilas,cantColumnas,1)
    for i in range(cantFilas):
        arrayAux = []
        for j in range(cantColumnas):
            arrayAux.append(0)
        arrayNormalizado.append(arrayAux)


    # Asignar 1 a la matriz
    # -1 cuando es >= y se agrega 1 a la variable artificial
    posicionVariableArtificial = restricciones

    for i in range(len(arrayNormalizado)):
        for j in range(len(arrayNormalizado[i])):
            arrayAux = []
            if i == j:
                if arrayRestricciones[i][variables] == 1:
                    arrayNormalizado[i][j] = 1
                    arrayNormalizado[i][posicionVariableArtificial] = -1
                    posicionVariableArtificial += 1
                else:
                    arrayNormalizado[i][j] = 1


    # Juntar la matriz variables/restricciones con la matriz normalizada
    for i in range(len(arrayRestricciones)):
        arrayAuxFilas = []
        for j in range(variables):
            arrayAuxFilas.append(arrayRestricciones[i][j])

        for k in range(len(arrayNormalizado[i])):
            arrayAuxFilas.append(arrayNormalizado[i][k])
        arrayFinal.append(arrayAuxFilas)

    cantColumnas += variables
    return arrayFinal,cantVariablesArtificiales,cantFilas,cantColumnas

def definirArrayCx(arrayRestricciones, restricciones,cantVariablesArtificiales,variables):
    contR= 1
    contS= 1
    contH= 1

    indiceRestricciones = 0 + variables
    indiceS = 0 + variables

    tamArray = restricciones+cantVariablesArtificiales+variables
    arrayNombreVariables = []
    arrayXb = []
    arrayBi = []
    arrayCj = []
    arrayCxCj = []


    for i in range(tamArray):
        arrayNombreVariables.append(0)
        arrayCj.append(0)
    
    for i in range(variables):
        arrayNombreVariables[i] = f'X{i}'

    for i in range(len(arrayRestricciones)):
        R = ""
        S = ""
        H = ""
        if(arrayRestricciones[i][variables] == 1):
            R = f'R{contR}'
            S = f'S{contS}'

            arrayNombreVariables[indiceRestricciones] = R
            arrayCj[indiceRestricciones] = 1
            arrayNombreVariables[restricciones+indiceS] = S
            arrayCj[restricciones+indiceS] = 0
            arrayXb.append(R)
            arrayCxCj.append(1)

            contR += 1
            contS += 1
            indiceRestricciones += 1
            indiceS += 1

        elif(arrayRestricciones[i][variables] == 2):
            H = f'H{contH}'
            arrayNombreVariables[indiceRestricciones] = H
            arrayCj[indiceRestricciones] = 0
            arrayXb.append(H)
            arrayCxCj.append(0)

            contH += 1
            indiceRestricciones += 1

        elif(arrayRestricciones[i][variables] == 3):
            R = f'R{contR}'
            arrayNombreVariables[indiceRestricciones] = R
            arrayCj[indiceRestricciones] = 1
            arrayXb.append(R)
            arrayCxCj.append(1)

            contR += 1
            indiceRestricciones += 1
        
        arrayBi.append(arrayRestricciones[i][variables+1])

    return arrayNombreVariables,arrayXb,arrayBi,arrayCj,arrayCxCj

def hallarZjCj(arrayCx,arrayCxCj,arrayCj):
    
    arrayZjCj = [] 
    for j in range(len(arrayCj)):
        sumador = 0
        for i in range(len(arrayCx)):
            sumador += arrayCxCj[i]*arrayCx[i][j]
        
        arrayZjCj.append(sumador-arrayCj[j])


    return arrayZjCj

def hallarZ(arrayBi,arrayCxCj):
    sumador = 0
    for i in range(len(arrayBi)):
        sumador+= (arrayBi[i]*arrayCxCj[i])

    return sumador

def puntoPivoteMinimizacion(arrayBi, arrayCx,arrayZjCj):
    valor= max(arrayZjCj)
    columna = arrayZjCj.index(valor)
    arrayAuxFila = []

    for i in range(len(arrayCx)):
        arrayAuxFila.append(arrayBi[i]/arrayCx[i][columna])

    valor = min(arrayAuxFila)
    fila = arrayAuxFila.index(valor)

    return fila,columna

def llenarDatosTablas(arrayCj,arrayNombreVariables,arrayXb,arrayCx,arrayZjCj,arrayCxCj,arrayBi,filaPivote,columnaPivote,valorPivote,arrayAuxTablas,posTabla):
    
    #LLENAR ARREGLO DE CX y Bi
    for i in range(len(arrayAuxTablas[posTabla][1])):
        if(i == filaPivote):
            for j in range(len(arrayAuxTablas[posTabla][1][i])):
                arrayCx[i][j] = arrayAuxTablas[posTabla][1][i][j]/valorPivote

            arrayBi[i] = arrayAuxTablas[posTabla][3][i]/valorPivote

    

    for i in range(len(arrayAuxTablas[posTabla][1])):
        if(i != filaPivote):
            datoPasarCero = (arrayAuxTablas[posTabla][1][i][columnaPivote] *-1)        
            for j in range(len(arrayAuxTablas[posTabla][1][i])):
                arrayCx[i][j] = (arrayCx[filaPivote][j]*datoPasarCero)+arrayAuxTablas[posTabla][1][i][j]

            arrayBi[i] = (arrayCx[filaPivote][j]*datoPasarCero)+arrayAuxTablas[posTabla][1][i][j]
            

    #SOBREESCRBIR ARREGLO Xb
    arrayXb[filaPivote] = arrayNombreVariables[columnaPivote]

    #SOBRESCRIBIR ARREGLO CxCj
    arrayCxCj[filaPivote] = arrayCj[columnaPivote]

    auxArrayZjCj = hallarZjCj(arrayCx,arrayCxCj,arrayCj)

    for i in range(len(auxArrayZjCj)):
        arrayZjCj[i]=auxArrayZjCj[i]

    resultadoZ = hallarZ(arrayBi,arrayCxCj)

    return arrayCj,arrayNombreVariables,arrayXb,arrayCx,arrayZjCj,arrayCxCj,arrayBi,resultadoZ



if __name__ == "__main__":
    #print("--------------")
    arrayAuxTablas = []
    arrayRestricciones = []
    arrayFO = []

    variables = int(input("Digite numero de variables: "))
    restricciones = int(input("Digite numero de restricciones: "))
    operacion = int(input("Digite 1=max 2=min "))
    arrayFO, arrayRestricciones = ingresarRestricciones(restricciones,variables)

    #FASE 1
    arrayCx,cantVariablesArtificiales,filas,columnaFase1 = definirMatriz(arrayRestricciones, variables, restricciones)
    arrayNombreVariables,arrayXb,arrayBi,arrayCj,arrayCxCj = definirArrayCx(arrayRestricciones, restricciones, cantVariablesArtificiales, variables)
    arrayZjCj = hallarZjCj(arrayCx,arrayCxCj,arrayCj)
    resultadoZ = hallarZ(arrayBi,arrayCxCj)

    arrayAuxTablas.append([arrayNombreVariables,arrayCx,arrayXb,arrayBi,arrayCj,arrayCxCj,arrayZjCj,resultadoZ])
    posTabla = 0


    if(resultadoZ == 0):
       #2fase

       print("entro")
    else:
        #Minimizacion
        if(operacion == 2):
            #validar si hay puntos positivos en el arreglo ZjCj
            contArrayZjCJPositivos = 0
            for i in range(len(arrayZjCj)):
                if(arrayZjCj[i]>0):
                    contArrayZjCJPositivos +=1

            #Realiza las tablas mientras que haya puntos positivos
            while(contArrayZjCJPositivos > 0):
                filaPivote,columnaPivote = puntoPivoteMinimizacion(arrayBi,arrayCx,arrayZjCj)

                valorPivote = arrayCx[filaPivote][columnaPivote]
                arrayCx = crearMatrizCeros(filas,columnaFase1,1)
                arrayZjCJ = crearMatrizCeros(filas,columnaFase1,3)
                arrayCxCj = crearMatrizCeros(filas,columnaFase1,2)
                arrayBi = crearMatrizCeros(filas,columnaFase1,2)

                arrayCj,arrayNombreVariables,arrayXb,arrayCx,arrayZjCj,arrayCxCj,arrayBi,resultadoZ =llenarDatosTablas(arrayCj,arrayNombreVariables,arrayXb,arrayCx,arrayZjCj,arrayCxCj,arrayBi,filaPivote,columnaPivote,valorPivote,arrayAuxTablas,posTabla)
                contArrayZjCJPositivos = 0
                for i in range(len(arrayZjCj)):
                    if(arrayZjCj[i]>0):
                        contArrayZjCJPositivos +=1
                
                arrayAuxTablas.append([arrayNombreVariables,arrayCx,arrayXb,arrayBi,arrayCj,arrayCxCj,arrayZjCj,resultadoZ])
                posTabla += 1

                print(posTabla)
                print(arrayAuxTablas);



            if(resultadoZ == 0):
                print("entro")


#### #

#### SOLUCIONAR ARREGLO Bi y CxCj para los resultados............