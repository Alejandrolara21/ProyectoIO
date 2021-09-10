from flask import request
from os import remove, path
import numpy as np
import random
import glob 
from matplotlib import pyplot as plt
from fractions import Fraction

# Funcion para obtener los valores de cada restricción
def obtenerRestricciones(restricciones):
    arrayRestricciones = []
    for i in range(restricciones):
        restriccionX = request.form.get(f'X{i}')
        restriccionX = round(pasarFraccionDecimal(restriccionX), 9)

        restriccionY = request.form.get(f'Y{i}')
        restriccionY = round(pasarFraccionDecimal(restriccionY),9)

        signo = request.form.get(f'S{i}')
        
        valor = request.form.get(f'R{i}')
        valor = round(pasarFraccionDecimal(valor),9)

        arrayAux = [float(restriccionX),float(restriccionY),signo,float(valor)]
        arrayRestricciones.append(arrayAux)
    return arrayRestricciones

# Permite obtener los valores de cada uno de las restricciones para hacer la comparacion y obtener los puntos de corte
def obtenerPuntosCorte(arrayRestricciones):
    arrayTotalPuntos = []
    for i in range(len(arrayRestricciones)-1):
        auxX = arrayRestricciones[i][0]
        auxY = arrayRestricciones[i][1]
        auxValor = arrayRestricciones[i][3]

        for j in range(len(arrayRestricciones)-1):
            j= j+i
            if j < len(arrayRestricciones)-1:
                auxX2 = arrayRestricciones[j+1][0]
                auxY2 = arrayRestricciones[j+1][1]
                auxValor2 = arrayRestricciones[j+1][3]
                obtenerValorPuntosCorte(arrayTotalPuntos, auxX,auxY,auxValor,auxX2,auxY2,auxValor2)
    return arrayTotalPuntos

#Obtiene las coordenadas para graficar las rectas
def obtenerCoordenadas(arrayRestricciones, arrayTotalPuntos):
    arrayPuntosNegativos = []
    arrayCategoriaPunto = []
    arrayPuntosGrafica = []
    arrayValidarPuntosGrafica = []

    for i in range(len(arrayRestricciones)):
        auxX = arrayRestricciones[i][0]
        auxY = arrayRestricciones[i][1]
        auxValor = arrayRestricciones[i][3]
        if auxX>0 and auxY>0:
            corX=round(hallarValorVariable(auxValor,auxX), 9)
            corY=round(hallarValorVariable(auxValor,auxY), 9)

            arrayPuntosGrafica.append([corX,0,0,corY])
            arrayValidarPuntosGrafica.append([corX,0])
            arrayValidarPuntosGrafica.append([0,corY])
            arrayTotalPuntos.append([corX,0])
            arrayTotalPuntos.append([0,corY])
            arrayCategoriaPunto.append(1)
        elif auxX==0 and auxY>0:
            corY=round(hallarValorVariable(auxValor,auxY), 9)

            arrayPuntosGrafica.append([0,corY])
            arrayValidarPuntosGrafica.append([0,corY])
            arrayTotalPuntos.append([0,corY])
            arrayCategoriaPunto.append(0)
        elif auxX>0 and auxY==0:
            corX=round(hallarValorVariable(auxValor,auxX),9)

            arrayPuntosGrafica.append([corX,0])
            arrayValidarPuntosGrafica.append([corX,0])
            arrayTotalPuntos.append([corX,0])
            arrayCategoriaPunto.append(0)
        elif auxX<0 and auxY>0:
            corY=round(hallarValorVariable(auxValor,auxY), 9)

            arrayPuntosNegativos.append([auxX,auxY,auxValor])
            arrayPuntosGrafica.append([0,corY])
            arrayValidarPuntosGrafica.append([0,corY])
            arrayTotalPuntos.append([0,corY])
            arrayCategoriaPunto.append(-1)
        elif auxX>0 and auxY<0:
            corX=round(hallarValorVariable(auxValor,auxX), 9)

            arrayPuntosNegativos.append([auxX,auxY,auxValor])
            arrayPuntosGrafica.append([corX,0])
            arrayValidarPuntosGrafica.append([corX,0])
            arrayTotalPuntos.append([corX,0])
            arrayCategoriaPunto.append(-1)

    arrayPuntosGrafica.append([0,0])
    arrayValidarPuntosGrafica.append([0,0])
    arrayTotalPuntos.append([0,0])

    return arrayPuntosGrafica, arrayValidarPuntosGrafica, arrayTotalPuntos, arrayPuntosNegativos, arrayCategoriaPunto

#Funcion que permite validar las restricciones
def validarRestricciones(funcionObjetivoX, funcionObjetivoY, arrayRestricciones, arrayTotalPuntos):
    arrayCategoriaFO = []
    arrayValorObjetivo = []
    resta = 0

    for j in range(len(arrayTotalPuntos)):
        acu= 0
        auxMayor= 0
        tMayor = 0
        pX= arrayTotalPuntos[j][0]
        pY= arrayTotalPuntos[j][1]

        for i in range(len(arrayRestricciones)):
            auxX = arrayRestricciones[i][0]
            auxY = arrayRestricciones[i][1]
            auxSig = arrayRestricciones[i][2]
            auxValor = arrayRestricciones[i][3]

            resultado = (auxX*pX)+(auxY*pY)
            resta = auxValor - resultado

            if(resta < 0):
                resta = resta * -1

            if(resta < 0.001):
                    resultado = auxValor

            if(auxSig == "<="):
                if(resultado <= auxValor):
                    acu+=1
            elif(auxSig == ">="):
                auxMayor+=1
                if(resultado >= auxValor):
                    acu+=1
            elif(auxSig == "="):
                if(resultado == auxValor):
                    acu+=1

        resultadoFO = round((float(funcionObjetivoX)*pX) + (float(funcionObjetivoY)*pY), 9)
        arrayValorObjetivo.append([pX, pY, resultadoFO])

        if(acu == len(arrayRestricciones)):
            arrayCategoriaFO.append(1)
        else:
            arrayCategoriaFO.append(0)

    if(auxMayor == len(arrayRestricciones)):
            tMayor = 1


    arrayPuntosRepetidos = []
    arrayBanderaPuntosRepetidos = []
    for i in range(len(arrayValorObjetivo)):
        if(arrayValorObjetivo[i] not in arrayPuntosRepetidos):
            arrayPuntosRepetidos.append(arrayValorObjetivo[i])
            arrayBanderaPuntosRepetidos.append(arrayCategoriaFO[i])

    arrayCategoriaFO = arrayBanderaPuntosRepetidos
    arrayValorObjetivo = arrayPuntosRepetidos 
    return arrayValorObjetivo, arrayCategoriaFO, tMayor

#Funcion que permite obtener la funcion objetivo
def obtenerFuncionObjetivo(operacion, arrayValorObjetivo, arrayCategoriaFO):
    auxIndex = -1;
    for i in range(len(arrayCategoriaFO)):
        if(arrayCategoriaFO[i] == 1 and arrayCategoriaFO[i] != 0):
            auxFO = arrayValorObjetivo[i][2]
            auxIndex = i

    if(auxIndex == -1):
        return

    if(operacion == "1"):
        for i in range(len(arrayCategoriaFO)):
            if(arrayCategoriaFO[i] == 1):
                if(auxFO < arrayValorObjetivo[i][2]):
                    auxFO = arrayValorObjetivo[i][2]
                    auxIndex = i

    elif(operacion == "2"):
        for i in range(len(arrayCategoriaFO)):
            if(arrayCategoriaFO[i] == 1):
                if(auxFO > arrayValorObjetivo[i][2]):
                    auxFO = arrayValorObjetivo[i][2]
                    auxIndex = i
    
    arrayCategoriaFO[auxIndex] = 2

    for i in range(len(arrayCategoriaFO)):
        if(auxFO == arrayValorObjetivo[i][2] and arrayCategoriaFO[i] == 1):
            arrayCategoriaFO[i] = 2

# Generar las rectas de las ecuaciones y mostrarlas.
def mostrarGrafica(arrayCategoriaPunto, arrayPuntosGrafica, arrayValidarPuntosGrafica, arrayPuntosNegativos, arrayCategoriaFO, arrayValorObjetivo, tMayor):
    plt.cla()   # Clear axis
    plt.clf()   # Clear figure
    maxX = 0
    maxY = 0

    contValores = 0
    for i in range(len(arrayCategoriaPunto)):
        if(arrayCategoriaPunto[i] == 1): #Cuando son dos coordenadas
            graficaX1 = arrayPuntosGrafica[i][0]
            graficaY1 = arrayPuntosGrafica[i][1]
            graficaX2 = arrayPuntosGrafica[i][2]
            graficaY2 = arrayPuntosGrafica[i][3]

            X = [graficaX1,graficaX2]
            Y = [graficaY1,graficaY2]
            plt.plot(X,Y,color="red")
        elif(arrayCategoriaPunto[i] == 0):#Cuando solo es una coordenada
            graficaX1 = arrayPuntosGrafica[i][0]
            graficaY1 = arrayPuntosGrafica[i][1]

            if(graficaX1>0 and graficaY1==0):
                X = [graficaX1]
                plt.axvline(X,color="blue")
            elif(graficaX1==0 and graficaY1>0):
                Y = [graficaY1]
                plt.axhline(Y,color="blue")
        elif(arrayCategoriaPunto[i] == -1):#Cuando algun punto negativo
            graficaX1 = arrayPuntosGrafica[i][0]
            graficaY1 = arrayPuntosGrafica[i][1]
 
            maximoX = arrayValidarPuntosGrafica[0][0]
            maximoY = arrayValidarPuntosGrafica[0][1]

            for j in range(len(arrayValidarPuntosGrafica)):
                if(maximoX < arrayValidarPuntosGrafica[j][0]):
                    maximoX = arrayValidarPuntosGrafica[j][0]

                if(maximoY < arrayValidarPuntosGrafica[j][1]):
                    maximoY = arrayValidarPuntosGrafica[j][1]

            if(graficaX1 > 0 and graficaY1 == 0):
                valorX= arrayPuntosNegativos[contValores][0]
                valorY= arrayPuntosNegativos[contValores][1]
                valorR= arrayPuntosNegativos[contValores][2]
                
                avalorX= valorX*maximoX
                resultadoY = hallarPuntoNegativo(valorR,valorY,avalorX)
                graficaX2 = maximoX
                graficaY2 = resultadoY
            elif(graficaY1 > 0 and graficaX1 == 0):
                valorX= arrayPuntosNegativos[contValores][0]
                valorY= arrayPuntosNegativos[contValores][1]
                valorR= arrayPuntosNegativos[contValores][2]
                
                avalorY= valorY*maximoY
                resultadoX = hallarPuntoNegativo(valorR,valorX,avalorY)
                graficaX2 = resultadoX
                graficaY2 = maximoY

            contValores += 1

            X = [graficaX1,graficaX2]
            Y = [graficaY1,graficaY2]

            plt.plot(X,Y,color="green")
    

# PINTAR EL AREA OPTIMA

    arrayAuxPuntosOptimosX = []
    arrayAuxPuntosOptimosY = []

    plt.ylim(bottom=0)
    plt.xlim(left=0)
    maxY=  plt.ylim(bottom=0)[1]
    maxX =  plt.xlim(left=0)[1]

    for i in range(len(arrayCategoriaFO)):
        if( arrayCategoriaFO[i] == 1 or arrayCategoriaFO[i] == 2):
            arrayAuxPuntosOptimosX.append(arrayValorObjetivo[i][0])
            arrayAuxPuntosOptimosY.append(arrayValorObjetivo[i][1])
            plt.plot(arrayValorObjetivo[i][0], arrayValorObjetivo[i][1], color='black', marker='o')

    arrayPuntosRandomX = []
    arrayPuntosRandomY = []



    if(tMayor == 1):
        arrayAuxPuntosOptimosX.append(maxX)
        arrayAuxPuntosOptimosY.append(maxY*100) 

        arrayAuxPuntosOptimosX.append(maxX*100)
        arrayAuxPuntosOptimosY.append(maxX) 

    for i in range(len(arrayAuxPuntosOptimosX)):
        for j in range(len(arrayAuxPuntosOptimosX)):
            if(i!=j and j>i):
                arrayPuntosRandomX.append(arrayAuxPuntosOptimosX[i])
                arrayPuntosRandomY.append(arrayAuxPuntosOptimosY[i])
                arrayPuntosRandomX.append(arrayAuxPuntosOptimosX[j])
                arrayPuntosRandomY.append(arrayAuxPuntosOptimosY[j])
                arrayPuntosRandomX.append(arrayAuxPuntosOptimosX[0])
                arrayPuntosRandomY.append(arrayAuxPuntosOptimosY[0])
                plt.fill(arrayPuntosRandomX,arrayPuntosRandomY,color='c')

    plt.grid()

    nombreImagen = "imagen"+str(random.randint(1,9999))
    if path.exists("static/img/"+nombreImagen+".jpg"):
        nombreImagen = "imagen"+str(random.randint(1,9999))

    plt.savefig("static/img/"+str(nombreImagen)+".jpg")

    return nombreImagen


# Funcion que permite obtener los puntos de corte de cada ecuación
def obtenerValorPuntosCorte(arrayTotalPuntos, x1,y1,valor1,x2,y2,valor2):
    arrayAuxPuntosCorte=[]
    valores = np.array([[x1,y1],[x2,y2]])
    resultado = np.array([valor1,valor2])

    try:
        arrayAuxPuntosCorte.append(np.linalg.solve(valores, resultado))
        if(arrayAuxPuntosCorte[0][0]>0 and arrayAuxPuntosCorte[0][1]>0):
            arrayAuxPuntosCorte[0][0] = round(arrayAuxPuntosCorte[0][0], 9)
            arrayAuxPuntosCorte[0][1] = round(arrayAuxPuntosCorte[0][1], 9)
            arrayTotalPuntos.append([arrayAuxPuntosCorte[0][0],arrayAuxPuntosCorte[0][1]])
    except:
        print("No tienen punto de corte") 

        
#Funcion para hallar el valor de X y Y despejando la ecuacion
def hallarValorVariable(auxValor, aux):
    return auxValor/aux

#Funcion que halla el valor de X y Y, cuando esta fuera del cuadrante 1
def hallarPuntoNegativo(auxValor, aux1, aux2):
    return (auxValor - aux2)/aux1


def pasarFraccionDecimal(dato):
    valor = 0
    if("/" in dato):
        dato = dato.split("/")
        numerador = dato[0]
        denominador = dato[1]
        valor = float(numerador)/float(denominador)
    else:
        valor = float(dato)

    return valor