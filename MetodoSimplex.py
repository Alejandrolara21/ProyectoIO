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

def definirMatriz(arrayRestricciones, arrayFO, variables, restricciones, operacion):
    cantColumnasVariables = 0
    cantFilas = 0
    cantVariablesArtificiales = 0
    arrayNormalizado = []
    arrayFinal = []

    # Si es minimizacion
    if operacion == 2:
        for i in range(len(arrayFO)):
            arrayFO[i] = arrayFO[i] * -1

    # Obteniendo filas y columnasvariables
    cantFilas = restricciones
    for i in range(len(arrayRestricciones)):
        if arrayRestricciones[i][variables] == 1:
            cantVariablesArtificiales+=1
    cantColumnasVariables = restricciones + cantVariablesArtificiales

    # Matriz de ceros
    for i in range(cantFilas):
        arrayAux = []
        for j in range(cantColumnasVariables):
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
                    arrayNormalizado[i][j] = -1
                    arrayNormalizado[i][posicionVariableArtificial] = 1
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

    return arrayFinal

if __name__ == "__main__":
    arrayRestricciones = []
    arrayFO = []
    arrayNormalizado = []

    variables = int(input("Digite numero de variables: "))
    restricciones = int(input("Digite numero de restricciones: "))
    operacion = int(input("Digite 1=max 2=min "))

    arrayFO, arrayRestricciones = ingresarRestricciones(restricciones,variables)
    arrayNormalizado = definirMatriz(arrayRestricciones, arrayFO, variables, restricciones, operacion)
    print(arrayNormalizado)