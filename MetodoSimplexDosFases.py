from flask import request
import numpy as np

def pasarFraccionDecimal(dato):
    dato = str(dato)
    valor = 0
    if("/" in dato):
        dato = dato.split("/")
        numerador = dato[0]
        denominador = dato[1]
        valor = float(numerador)/float(denominador)
    else:
        valor = float(dato)

    return valor

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

# Permite obtener los valores del arreglo ZjCj
def hallarZjCj(arrayCx,arrayCxCj,arrayCj):
    arrayZjCj = [] 
    for j in range(len(arrayCj)):
        sumador = 0
        for i in range(len(arrayCx)):
            sumador += arrayCxCj[i]*arrayCx[i][j]
        arrayZjCj.append(sumador-arrayCj[j])

    return arrayZjCj

# Permite obtener el valor de Z
def hallarZ(arrayBi,arrayCxCj):
    sumador = 0
    for i in range(len(arrayBi)):
        sumador+= (arrayBi[i]*arrayCxCj[i])
    return sumador

# Funcion que permite recibir los valores de las restricciones y variables
def ingresarRestricciones(cantRestricciones,cantVariables):
    arrayFO = []
    for i in range(cantVariables):
        datoFO = request.form.get(f'F{i}')
        datoFO = round(pasarFraccionDecimal(datoFO), 9)
        
        arrayFO.append(float(datoFO))

    arrayRestricciones = []

    for i in range(cantRestricciones):
        arrayAux = []
        for j in range(cantVariables):
            datoRestricciones = request.form.get(f'R{i}_V{j}')
            datoRestricciones = round(pasarFraccionDecimal(datoRestricciones), 9)

            arrayAux.append(float(datoRestricciones))

        signoRestriccion = request.form.get(f'S{i}')
        valorRestriccion = request.form.get(f'V{i}')
        valorRestriccion = round(pasarFraccionDecimal(valorRestriccion), 9)

        if(valorRestriccion < 0):
            valorRestriccion = valorRestriccion*(-1)
            
            if(signoRestriccion == "1"):
                signoRestriccion = "2"
            elif(signoRestriccion == "2"):
                signoRestriccion = "1"
            
            for z in range(len(arrayAux)):
                arrayAux[z] = arrayAux[z]*(-1)


        arrayAux.append(int(signoRestriccion))
        arrayAux.append(float(valorRestriccion))
        arrayRestricciones.append(arrayAux)

    return arrayFO, arrayRestricciones

# Permite crear la el arreglo Cx con los valores de las variables y sus variables de holgura, superavit y variables artificiales
def definirMatrizInicial(arrayRestricciones, variables, restricciones):
    
    cantColumnas = 0
    cantFilas = 0
    cantVariablesArtificiales = 0
    arrayNormalizado = []
    arrayCx = []

    # Obteniendo filas y columnas para las varibles de holgura, superavit y artificiales
    cantFilas = restricciones

    for i in range(len(arrayRestricciones)):
        #Obtenemos el signo >= para aumentar el tamaño de columnas
        if arrayRestricciones[i][variables] == 1:
            cantVariablesArtificiales+=1
    cantColumnas = restricciones + cantVariablesArtificiales

    #Llamamos la funcion crearMatrizCeros para crear un arreglo en 0 con el tamaño de filas y columnas que se envian
    arrayNormalizado = crearMatrizCeros(cantFilas,cantColumnas,1)

    # Asignar 1 a la matriz
    # -1 cuando es >= y se agrega 1 a la variable artificial
    posicionVariableArtificial = restricciones

    for i in range(len(arrayNormalizado)):
        for j in range(len(arrayNormalizado[i])):
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
        arrayCx.append(arrayAuxFilas)

    #A la cantidad de las columnas se le suma la cantidad de variables para tener el tamaño completo de la matriz
    cantColumnas += variables

    return arrayCx,cantVariablesArtificiales,cantFilas,cantColumnas

# Esta funcion permite crear los arreglos que guardaran diferente informacion
# Los arreglos creados son: arrayNombreVariables,arrayXb,arrayBi,arrayCj,arrayCxCj. 
def definirArreglosInicialesTabla(arrayRestricciones, restricciones,cantVariablesArtificiales,variables,operacion):
    #Contadores que permiten saber el numero de la variable de holgura (H), superavit (S) y artificil (R)
    contR= 1
    contS= 1
    contH= 1
    #indice para las posicion de las variables de superavit que se pondran en el final
    indiceRestricciones = 0 + variables
    indiceS = 0 + variables

    tamArray = restricciones+cantVariablesArtificiales+variables
    arrayNombreVariables = []
    arrayXb = []
    arrayBi = []
    arrayCj = []
    arrayCxCj = []

    arrayCj = crearMatrizCeros(restricciones,tamArray,3)
    arrayNombreVariables = crearMatrizCeros(restricciones,tamArray,3)
    
    for i in range(variables):
        arrayNombreVariables[i] = f'X{i+1}'

    for i in range(len(arrayRestricciones)):
        R = ""
        S = ""
        H = ""
        if(arrayRestricciones[i][variables] == 1):
            R = f'R{contR}'
            S = f'S{contS}'

            arrayNombreVariables[indiceRestricciones] = R
            if(operacion == 1):
                arrayCj[indiceRestricciones] = -1
                arrayCxCj.append(-1)
            elif(operacion == 2):
                arrayCj[indiceRestricciones] = 1
                arrayCxCj.append(1)
            
            arrayNombreVariables[restricciones+indiceS] = S
            arrayCj[restricciones+indiceS] = 0
            arrayXb.append(R)

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
            if(operacion == 1):
                arrayCj[indiceRestricciones] = -1
                arrayCxCj.append(-1)
            elif(operacion == 2):
                arrayCj[indiceRestricciones] = 1
                arrayCxCj.append(1)
            arrayXb.append(R)


            contR += 1
            indiceRestricciones += 1
        
        arrayBi.append(arrayRestricciones[i][variables+1])

    return arrayNombreVariables,arrayXb,arrayBi,arrayCj,arrayCxCj

# Obtiene el punto pivote de la tabla cuando la operacion es minimizacion
def puntoPivoteMinimizacion(arrayBi, arrayCx,arrayZjCj):
    valor = max(arrayZjCj)
    columna = arrayZjCj.index(valor)
    arrayAuxFila = []   
    
    for i in range(len(arrayCx)):
        resultado = 0
        try:
            resultado = arrayBi[i]/arrayCx[i][columna]
            arrayAuxFila.append(resultado)
        except:
            arrayAuxFila.append(resultado)

    valorFila =  max(arrayAuxFila)
    fila = arrayAuxFila.index(valorFila)

    for i in range(len(arrayAuxFila)):
        if(arrayAuxFila[i] < valorFila and arrayAuxFila[i] > 0):
            valorFila = arrayAuxFila[i]
            fila = i   

    return fila,columna

# Validar si continua realizando las tablas para la operacion minimizacion
def validarZjCjMinimizacion(arrayZjCj):
    contArrayZjCJPositivos = 0
    for i in range(len(arrayZjCj)):
        if(arrayZjCj[i]>0):
            contArrayZjCJPositivos +=1
    return contArrayZjCJPositivos

#Funcion que genera las tablas que se van formando de las tablas anteriores haciendo gauss jordan
def llenarDatosTablas(arrayCj,arrayNombreVariables,arrayXb,arrayCx,arrayZjCj,arrayCxCj,arrayBi,filaPivote,columnaPivote,valorPivote,arrayAuxTablas,posTabla):
    #LLENAR ARREGLO DE Cx y Bi
    for i in range(len(arrayAuxTablas[posTabla][1])):
        if(i == filaPivote):
            for j in range(len(arrayAuxTablas[posTabla][1][i])):
                try:
                    arrayCx[i][j] = arrayAuxTablas[posTabla][1][i][j]/valorPivote
                except:
                    arrayCx[i][j] = 0
            try:
                arrayBi[i] = arrayAuxTablas[posTabla][3][i]/valorPivote
            except:
                arrayBi[i] = 0
    for i in range(len(arrayAuxTablas[posTabla][1])):
        if(i != filaPivote):
            datoPasarCero = (arrayAuxTablas[posTabla][1][i][columnaPivote] *-1)
        
            for j in range(len(arrayAuxTablas[posTabla][1][i])):
                arrayCx[i][j] = (arrayCx[filaPivote][j]*datoPasarCero)+arrayAuxTablas[posTabla][1][i][j]
            arrayBi[i] = (arrayBi[filaPivote]*datoPasarCero)+arrayAuxTablas[posTabla][3][i]
    #SOBREESCRBIR ARREGLO Xb
    arrayXb[filaPivote] = arrayNombreVariables[columnaPivote] #######-------------
    for i in range(len(arrayXb)):
        if( i != filaPivote):
            arrayXb[i] = arrayAuxTablas[posTabla][2][i]

    #SOBRESCRIBIR ARREGLO CxCj
    arrayCxCj[filaPivote] = arrayCj[columnaPivote]
    for i in range(len(arrayCxCj)):
        if( i != filaPivote):
            arrayCxCj[i] = arrayAuxTablas[posTabla][5][i]

    #HALLAR ZjCj
    auxArrayZjCj = []
    auxArrayZjCj = hallarZjCj(arrayCx,arrayCxCj,arrayCj)
    for i in range(len(auxArrayZjCj)):
        arrayZjCj[i]=auxArrayZjCj[i]

    #HALLAR Z
    resultadoZ = hallarZ(arrayBi,arrayCxCj)
    
    return arrayCj,arrayNombreVariables,arrayXb,arrayCx,arrayZjCj,arrayCxCj,arrayBi,resultadoZ

def eliminarColumnaR(arrayTabla,arrayFO,variables):   
    arrayIndicesBorrar = []

    for i in range(len(arrayTabla[4])):
        if(arrayTabla[4][i] == 1 or arrayTabla[4][i] == -1):
            arrayIndicesBorrar.append(i)

    columnas = len(arrayTabla[4]) - len(arrayIndicesBorrar)
    
    arrayAuxCj = arrayTabla[4]
    arrayAuxCx = arrayTabla[1]
    arrayAuxNombreVariables = arrayTabla[0]
    
    arrayAuxCx = np.delete(arrayAuxCx,(arrayIndicesBorrar),axis=1)
    arrayAuxCj = np.delete(arrayAuxCj,(arrayIndicesBorrar))
    arrayAuxNombreVariables = np.delete(arrayAuxNombreVariables,(arrayIndicesBorrar))

    arrayCj = []
    arrayCx = []
    arrayNombreVariables = []

    for i in range(len(arrayAuxCj)):
        arrayCj.append(arrayAuxCj[i])
        arrayNombreVariables.append(arrayAuxNombreVariables[i])

    for i in range(len(arrayFO)):
        arrayCj[i] = arrayFO[i]

    for i in range(len(arrayAuxCx)):
        auxColumna = []
        for j in range(len(arrayAuxCx[i])):
            auxColumna.append(arrayAuxCx[i][j])
        arrayCx.append(auxColumna)

    return arrayCj,arrayCx,arrayNombreVariables,columnas

def definirNuevaCxCj(arrayNombreVariables, arrayXb,arrayCj):
    arrayAuxCxCj = [] 
    for j in range(len(arrayXb)):
        for i in range(len(arrayNombreVariables)):
            if(arrayNombreVariables[i] == arrayXb[j]):
                arrayAuxCxCj.append(arrayCj[i])
    return arrayAuxCxCj

def fase2Minimizacion(resultadoZ,arrayAuxGuardarTabla,arrayXb,arrayBi,arrayFO,variables,filas):
    mensaje= ""
    arrayPivoteAux = []
    if(resultadoZ == 0):
        arrayTablasFaseDos = []
        posTablaFase2 = 0
        arrayCj,arrayCx,arrayNombreVariables,columnaFase2 = eliminarColumnaR(arrayAuxGuardarTabla,arrayFO,variables)

        arrayCxCj = definirNuevaCxCj(arrayNombreVariables, arrayXb,arrayCj)
        arrayZjCj = hallarZjCj(arrayCx,arrayCxCj,arrayCj)
        resultadoZ = hallarZ(arrayBi,arrayCxCj)
        
        arrayAuxGuardarTabla = []
        arrayAuxGuardarTabla = [arrayNombreVariables,arrayCx,arrayXb,arrayBi,arrayCj,arrayCxCj,arrayZjCj,resultadoZ]
        arrayTablasFaseDos.append(arrayAuxGuardarTabla)

        contArrayZjCJPositivos = validarZjCjMinimizacion(arrayZjCj)

        while(contArrayZjCJPositivos > 0):
            filaPivote,columnaPivote = puntoPivoteMinimizacion(arrayBi,arrayCx,arrayZjCj)

            arrayPivoteAux.append([filaPivote,columnaPivote])

            valorPivote = arrayCx[filaPivote][columnaPivote]
            arrayCx = crearMatrizCeros(filas,columnaFase2,1)
            arrayZjCj = crearMatrizCeros(filas,columnaFase2,3)
            arrayCxCj = crearMatrizCeros(filas,columnaFase2,2)
            arrayBi = crearMatrizCeros(filas,columnaFase2,2)
            arrayXb = crearMatrizCeros(filas,columnaFase2,2)

            arrayCj,arrayNombreVariables,arrayXb,arrayCx,arrayZjCj,arrayCxCj,arrayBi,resultadoZ =llenarDatosTablas(arrayCj,arrayNombreVariables,arrayXb,arrayCx,arrayZjCj,arrayCxCj,arrayBi,filaPivote,columnaPivote,valorPivote,arrayTablasFaseDos,posTablaFase2)
            
            arrayAuxGuardarTabla = []
            arrayAuxGuardarTabla = [arrayNombreVariables,arrayCx,arrayXb,arrayBi,arrayCj,arrayCxCj,arrayZjCj,resultadoZ]
            arrayTablasFaseDos.append(arrayAuxGuardarTabla)
            posTablaFase2 += 1
            #validar si hay puntos positivos en el arreglo ZjCj
            contArrayZjCJPositivos = validarZjCjMinimizacion(arrayZjCj)
    else:
        mensaje ="Problema indefinido, sin solucion"
        arrayTablasFaseDos = []
    
    return mensaje,arrayTablasFaseDos,arrayPivoteAux

def fase2Maximizacion(resultadoZ,arrayAuxGuardarTabla,arrayXb,arrayBi,arrayFO,variables,filas):
    mensaje= ""
    arrayPivoteAux = []
    if(resultadoZ == 0):
        arrayTablasFaseDos = []
        posTablaFase2 = 0
        arrayCj,arrayCx,arrayNombreVariables,columnaFase2 = eliminarColumnaR(arrayAuxGuardarTabla,arrayFO,variables)

        arrayCxCj = definirNuevaCxCj(arrayNombreVariables, arrayXb,arrayCj)
        arrayZjCj = hallarZjCj(arrayCx,arrayCxCj,arrayCj)
        resultadoZ = hallarZ(arrayBi,arrayCxCj)
        
        arrayAuxGuardarTabla = []
        arrayAuxGuardarTabla = [arrayNombreVariables,arrayCx,arrayXb,arrayBi,arrayCj,arrayCxCj,arrayZjCj,resultadoZ]
        arrayTablasFaseDos.append(arrayAuxGuardarTabla)

        contArrayZjCJPositivos = validarZjCjMaximizacion(arrayZjCj)

        while(contArrayZjCJPositivos > 0):
            filaPivote,columnaPivote = puntoPivoteMaximizacion(arrayBi,arrayCx,arrayZjCj)

            arrayPivoteAux.append([filaPivote,columnaPivote])

            valorPivote = arrayCx[filaPivote][columnaPivote]
            arrayCx = crearMatrizCeros(filas,columnaFase2,1)
            arrayZjCj = crearMatrizCeros(filas,columnaFase2,3)
            arrayCxCj = crearMatrizCeros(filas,columnaFase2,2)
            arrayBi = crearMatrizCeros(filas,columnaFase2,2)
            arrayXb = crearMatrizCeros(filas,columnaFase2,2)

            arrayCj,arrayNombreVariables,arrayXb,arrayCx,arrayZjCj,arrayCxCj,arrayBi,resultadoZ = llenarDatosTablas(arrayCj,arrayNombreVariables,arrayXb,arrayCx,arrayZjCj,arrayCxCj,arrayBi,filaPivote,columnaPivote,valorPivote,arrayTablasFaseDos,posTablaFase2)
            
            arrayAuxGuardarTabla = []
            arrayAuxGuardarTabla = [arrayNombreVariables,arrayCx,arrayXb,arrayBi,arrayCj,arrayCxCj,arrayZjCj,resultadoZ]
            arrayTablasFaseDos.append(arrayAuxGuardarTabla)
            posTablaFase2 += 1
            #validar si hay puntos positivos en el arreglo ZjCj
            contArrayZjCJPositivos = validarZjCjMaximizacion(arrayZjCj)
    else:
        arrayTablasFaseDos=[]
        mensaje ="problema indefinido, sin solucion"
    
    return mensaje,arrayTablasFaseDos,arrayPivoteAux

def fase1Minimizacion(contArrayZjCJPositivos,posTablaFase1,arrayBi,arrayCx,arrayZjCj,arrayCj,arrayNombreVariables,arrayAuxTablas,filas,columnaFase1):
    arrayPivoteAux = []
    #Realiza las tablas mientras que haya puntos positivos
    band = 0
    while(contArrayZjCJPositivos > 0):
        filaPivote,columnaPivote = puntoPivoteMinimizacion(arrayBi,arrayCx,arrayZjCj)

        arrayPivoteAux.append([filaPivote,columnaPivote])

        valorPivote = arrayCx[filaPivote][columnaPivote]
        arrayCx = crearMatrizCeros(filas,columnaFase1,1)
        arrayZjCj = crearMatrizCeros(filas,columnaFase1,3)
        arrayCxCj = crearMatrizCeros(filas,columnaFase1,2)
        arrayBi = crearMatrizCeros(filas,columnaFase1,2)
        arrayXb = crearMatrizCeros(filas,columnaFase1,2)

        arrayCj,arrayNombreVariables,arrayXb,arrayCx,arrayZjCj,arrayCxCj,arrayBi,resultadoZ = llenarDatosTablas(arrayCj,arrayNombreVariables,arrayXb,arrayCx,arrayZjCj,arrayCxCj,arrayBi,filaPivote,columnaPivote,valorPivote,arrayAuxTablas,posTablaFase1)
        
        arrayAuxGuardarTabla = []
        arrayAuxGuardarTabla = [arrayNombreVariables,arrayCx,arrayXb,arrayBi,arrayCj,arrayCxCj,arrayZjCj,resultadoZ]
        arrayAuxTablas.append(arrayAuxGuardarTabla)
        posTablaFase1 += 1
        #validar si hay puntos positivos en el arreglo ZjCj
        contArrayZjCJPositivos = validarZjCjMinimizacion(arrayZjCj)
        if (band == 10):
            contArrayZjCJPositivos = 0

    return arrayAuxGuardarTabla,arrayAuxTablas,arrayNombreVariables,arrayCx,arrayXb,arrayBi,arrayCj,arrayCxCj,arrayZjCj,resultadoZ,arrayPivoteAux

def fase1Maximizacion(contArrayZjCJPositivos,posTablaFase1,arrayBi,arrayCx,arrayZjCj,arrayCj,arrayNombreVariables,arrayAuxTablas,filas,columnaFase1):
    #Realiza las tablas mientras que haya puntos positivos
    arrayPivoteAux = []
    arrayAuxGuardarTabla = []

    band = 0
    while(contArrayZjCJPositivos > 0):
        filaPivote,columnaPivote = puntoPivoteMaximizacion(arrayBi,arrayCx,arrayZjCj)

        arrayPivoteAux.append([filaPivote,columnaPivote])

        valorPivote = arrayCx[filaPivote][columnaPivote]
        arrayCx = crearMatrizCeros(filas,columnaFase1,1)
        arrayZjCj = crearMatrizCeros(filas,columnaFase1,3)
        arrayCxCj = crearMatrizCeros(filas,columnaFase1,2)
        arrayBi = crearMatrizCeros(filas,columnaFase1,2)
        arrayXb = crearMatrizCeros(filas,columnaFase1,2)

        arrayCj,arrayNombreVariables,arrayXb,arrayCx,arrayZjCj,arrayCxCj,arrayBi,resultadoZ = llenarDatosTablas(arrayCj,arrayNombreVariables,arrayXb,arrayCx,arrayZjCj,arrayCxCj,arrayBi,filaPivote,columnaPivote,valorPivote,arrayAuxTablas,posTablaFase1)
        
        arrayAuxGuardarTabla = []
        arrayAuxGuardarTabla = [arrayNombreVariables,arrayCx,arrayXb,arrayBi,arrayCj,arrayCxCj,arrayZjCj,resultadoZ]
        arrayAuxTablas.append(arrayAuxGuardarTabla)
        posTablaFase1 += 1
        #validar si hay puntos positivos en el arreglo ZjCj
        contArrayZjCJPositivos = validarZjCjMaximizacion(arrayZjCj)
        band += 1
        if (band == 10):
            contArrayZjCJPositivos = 0

    return arrayAuxGuardarTabla,arrayAuxTablas,arrayNombreVariables,arrayCx,arrayXb,arrayBi,arrayCj,arrayCxCj,arrayZjCj,resultadoZ,arrayPivoteAux

def puntoPivoteMaximizacion(arrayBi,arrayCx,arrayZjCj):
    valor= min(arrayZjCj)
    columna = arrayZjCj.index(valor)

    arrayAuxFila = []
    
    for i in range(len(arrayCx)):
        resultado = 0
        try:
            resultado = arrayBi[i]/arrayCx[i][columna]
            arrayAuxFila.append(resultado)
        except:
            arrayAuxFila.append(resultado)

    valorFila =  max(arrayAuxFila)
    fila = arrayAuxFila.index(valorFila)

    for i in range(len(arrayAuxFila)):
        if(arrayAuxFila[i] < valorFila and arrayAuxFila[i] > 0):
            valorFila = arrayAuxFila[i]
            fila = i 

    return fila,columna

def validarZjCjMaximizacion(arrayZjCj):
    contArrayZjCJPositivos = 0
    for i in range(len(arrayZjCj)):
        if(arrayZjCj[i]<0):
            contArrayZjCJPositivos +=1
    return contArrayZjCJPositivos

# if __name__ == "__main__":
#     #print("--------------")
#     arrayTablasFase1 = []
#     arrayRestricciones = []
#     arrayFO = []

#     variables = int(input("Digite numero de variables: "))
#     restricciones = int(input("Digite numero de restricciones: "))
#     operacion = int(input("Digite 1=max 2=min "))
#     arrayFO, arrayRestricciones = ingresarRestricciones(restricciones,variables)

#     #FASE 1
#     arrayCx,cantVariablesArtificiales,filas,columnaFase1 = definirMatrizInicial(arrayRestricciones, variables, restricciones)
#     arrayNombreVariables,arrayXb,arrayBi,arrayCj,arrayCxCj = definirArreglosInicialesTabla(arrayRestricciones, restricciones, cantVariablesArtificiales, variables,operacion)
#     arrayZjCj = hallarZjCj(arrayCx,arrayCxCj,arrayCj)
#     resultadoZ = hallarZ(arrayBi,arrayCxCj)

#     arrayUltimaTablaFase1 = []
#     arrayUltimaTablaFase1 = [arrayNombreVariables,arrayCx,arrayXb,arrayBi,arrayCj,arrayCxCj,arrayZjCj,resultadoZ]
#     arrayTablasFase1.append(arrayUltimaTablaFase1)
#     posTablaFase1 = 0

    # if(resultadoZ == 0):
    #     #FASE 1
    #     if(operacion ==1):
    #         #Maximizacion
    #         #FASE 2
    #         mensaje,arrayTablasFase2 = fase2Maximizacion(resultadoZ,arrayUltimaTablaFase1,arrayXb,arrayBi,arrayFO,variables,filas)
    #         print(arrayTablasFase2)
    #     elif(operacion == 2):
    #         #Minimizacion
    #         #FASE 2
    #         mensaje,arrayTablasFase2 = fase2Minimizacion(resultadoZ,arrayUltimaTablaFase1,arrayXb,arrayBi,arrayFO,variables,filas)
    #         print(arrayTablasFase2)
    # else:
    #     #FASE 1
    #     if(operacion ==1):
    #         #Maximizacion
    #         contArrayZjCJPositivos = validarZjCjMaximizacion(arrayZjCj)
    #         arrayUltimaTablaFase1,arrayTablasFase1,arrayNombreVariables,arrayCx,arrayXb,arrayBi,arrayCj,arrayCxCj,arrayZjCj,resultadoZ = fase1Maximizacion(contArrayZjCJPositivos,posTablaFase1,arrayBi,arrayCx,arrayZjCj,arrayCj,arrayNombreVariables,arrayTablasFase1,filas,columnaFase1)
    #         print(arrayTablasFase1)
    #         #FASE 2
    #         mensaje,arrayTablasFase2 = fase2Maximizacion(resultadoZ,arrayUltimaTablaFase1,arrayXb,arrayBi,arrayFO,variables,filas)
    #         print(arrayTablasFase2)
    #     elif(operacion == 2):
    #         #Minimizacion
    #         #validar si hay puntos positivos en el arreglo ZjCj
    #         contArrayZjCJPositivos = validarZjCjMinimizacion(arrayZjCj)
    #         arrayUltimaTablaFase1,arrayTablasFase1,arrayNombreVariables,arrayCx,arrayXb,arrayBi,arrayCj,arrayCxCj,arrayZjCj,resultadoZ = fase1Minimizacion(contArrayZjCJPositivos,posTablaFase1,arrayBi,arrayCx,arrayZjCj,arrayCj,arrayNombreVariables,arrayTablasFase1,filas,columnaFase1)
    #         print(arrayTablasFase1)
    #         #FASE 2
    #         mensaje,arrayTablasFase2 = fase2Minimizacion(resultadoZ,arrayUltimaTablaFase1,arrayXb,arrayBi,arrayFO,variables,filas)
    #         print(arrayTablasFase2)

        

##### SOLUCIONAR PIVOTE DE MAXIMIZACION #####