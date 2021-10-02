from flask import Flask, render_template, request
from matplotlib import pyplot as plt
from numpy.lib.function_base import percentile

plt.switch_backend('agg')

from MetodoGrafico import *
from MetodoSimplexDosFases import *

app = Flask(__name__)

@app.route('/')
def home():
    if len(glob.glob("static/img/*.jpg")) > 10:
        for archivo in glob.glob("static/img/*.jpg"):
            try:
                remove(archivo)
            except OSError as e:
                print(f"Error:{e.strerror}")
                
    return render_template("index.html")

@app.route('/metodoSimplexDosFases')
def metodoSimplexDosFases():
    return render_template("metodoSimplexDosFases.html")

@app.route('/procesarDosFases', methods=['GET'])
def procesarDosFases():
    operacion = 0
    cantidadRestricciones = 0
    cantidadVariables = 0

    operacion = request.args.get("metodo")
    cantidadRestricciones = int(request.args.get("restricciones"))
    cantidadVariables = int(request.args.get("variables"))


    return render_template("restriccionesDosFases.html", cantidadRestricciones=cantidadRestricciones, operacion=operacion,cantidadVariables=cantidadVariables)

@app.route('/realizarProcesoDosFases',methods=['POST'])
def realizarProcesoDosFases():
    arrayTablasFase1 = []
    arrayRestricciones = []
    arrayFO = []
    arrayPivoteFase1 = []
    arrayPivoteFase2 = []

    cantidadRestricciones = int(request.form.get("cantidadRestricciones"))
    cantidadVariables = int(request.form.get("cantidadVariables"))
    operacion = int(request.form.get("metodo"))

    arrayFO, arrayRestricciones = ingresarRestricciones(cantidadRestricciones,cantidadVariables)
    arrayCx,cantVariablesArtificiales,filas,columnaFase1 = definirMatrizInicial(arrayRestricciones, cantidadVariables, cantidadRestricciones)
    arrayNombreVariables,arrayXb,arrayBi,arrayCj,arrayCxCj = definirArreglosInicialesTabla(arrayRestricciones, cantidadRestricciones, cantVariablesArtificiales, cantidadVariables,operacion)
    arrayZjCj = hallarZjCj(arrayCx,arrayCxCj,arrayCj)
    resultadoZ = hallarZ(arrayBi,arrayCxCj)
    
    arrayUltimaTablaFase1 = []
    arrayUltimaTablaFase1 = [arrayNombreVariables,arrayCx,arrayXb,arrayBi,arrayCj,arrayCxCj,arrayZjCj,resultadoZ]
    arrayTablasFase1.append(arrayUltimaTablaFase1)
    posTablaFase1 = 0

    if(resultadoZ == 0):
        #FASE 1
        if(operacion ==1):
            #Maximizacion
            #FASE 2
            mensaje,arrayTablasFase2,arrayPivoteFase2 = fase2Maximizacion(resultadoZ,arrayUltimaTablaFase1,arrayXb,arrayBi,arrayFO,cantidadVariables,filas)
        elif(operacion == 2):
            #Minimizacion
            #FASE 2
            mensaje,arrayTablasFase2,arrayPivoteFase2= fase2Minimizacion(resultadoZ,arrayUltimaTablaFase1,arrayXb,arrayBi,arrayFO,cantidadVariables,filas)
    else:
        #FASE 1
        if(operacion ==1):
            #Maximizacion
            contArrayZjCJPositivos = validarZjCjMaximizacion(arrayZjCj)
            arrayUltimaTablaFase1,arrayTablasFase1,arrayNombreVariables,arrayCx,arrayXb,arrayBi,arrayCj,arrayCxCj,arrayZjCj,resultadoZ,arrayPivoteFase1 = fase1Maximizacion(contArrayZjCJPositivos,posTablaFase1,arrayBi,arrayCx,arrayZjCj,arrayCj,arrayNombreVariables,arrayTablasFase1,filas,columnaFase1)
            #FASE 2
            mensaje,arrayTablasFase2,arrayPivoteFase2 = fase2Maximizacion(resultadoZ,arrayUltimaTablaFase1,arrayXb,arrayBi,arrayFO,cantidadVariables,filas)
        elif(operacion == 2):
            #Minimizacion
            #validar si hay puntos positivos en el arreglo ZjCj
            contArrayZjCJPositivos = validarZjCjMinimizacion(arrayZjCj)
            arrayUltimaTablaFase1,arrayTablasFase1,arrayNombreVariables,arrayCx,arrayXb,arrayBi,arrayCj,arrayCxCj,arrayZjCj,resultadoZ,arrayPivoteFase1 = fase1Minimizacion(contArrayZjCJPositivos,posTablaFase1,arrayBi,arrayCx,arrayZjCj,arrayCj,arrayNombreVariables,arrayTablasFase1,filas,columnaFase1)
            #FASE 2
            mensaje,arrayTablasFase2,arrayPivoteFase2 = fase2Minimizacion(resultadoZ,arrayUltimaTablaFase1,arrayXb,arrayBi,arrayFO,cantidadVariables,filas)

    arrayPivoteFase1.append([-1,-1])
    arrayPivoteFase2.append([-1,-1])

    
    arrayFraccionesFase1 = []
    arrayFraccionesFase2 = []

    arrayFraccionesFase1 = pasarFraccionariosFases(arrayTablasFase1)
    arrayFraccionesFase2 = pasarFraccionariosFases(arrayTablasFase2)
    tamañoFase2 = len(arrayTablasFase2)-1


    arrayFraccionesFO = []
    for i in range(len(arrayFO)):
        arrayFraccionesFO.append(str(Fraction(arrayFO[i]).limit_denominator()))



    #arrayUltimaTablaFase1 = [arrayNombreVariables,arrayCx,arrayXb,arrayBi,arrayCj,arrayCxCj,arrayZjCj,resultadoZ]
    return render_template("dosFases.html",arrayTablasFase1=arrayTablasFase1,arrayTablasFase2=arrayTablasFase2,mensaje=mensaje,arrayFO=arrayFO,arrayPivoteFase1=arrayPivoteFase1,arrayPivoteFase2=arrayPivoteFase2, arrayFraccionesFase1=arrayFraccionesFase1, 
    arrayFraccionesFase2=arrayFraccionesFase2,tamañoFase2=tamañoFase2,arrayFraccionesFO=arrayFraccionesFO,operacion=operacion,cantidadVariables=cantidadVariables,cantidadRestricciones=cantidadRestricciones,arrayRestricciones=arrayRestricciones)

def pasarFraccionariosFases(arrayFase):
    arrayFraccionesFase = []
    for i in range(len(arrayFase)):
        auxArrayNombreVariables = []
        auxArrayCx = []
        auxArrayCj = []
        auxArrayXb = []
        auxArrayBi = []
        auxArrayCxCj = []
        auxArrayZjCj = []
        auxResultadoZ = 0
        for j in range(len(arrayFase[i][0])):
            auxArrayNombreVariables.append(arrayFase[i][0][j])
    
        for j in range(len(arrayFase[i][1])):
            arrayAuxFila = []
        
            for k in range(len(arrayFase[i][1][j])):
                aux1 = str(Fraction(arrayFase[i][1][j][k]).limit_denominator())
                arrayAuxFila.append(aux1)
            auxArrayCx.append(arrayAuxFila)
        
        for j in range(len(arrayFase[i][2])):
            auxArrayXb.append(arrayFase[i][2][j])
        
        for j in range(len(arrayFase[i][3])):
            aux1 = str(Fraction(arrayFase[i][3][j]).limit_denominator())
            auxArrayBi.append(aux1)
        
        for j in range(len(arrayFase[i][4])):
            aux1 = str(Fraction(arrayFase[i][4][j]).limit_denominator())
            auxArrayCj.append(aux1)

        for j in range(len(arrayFase[i][5])):
            aux1 = str(Fraction(arrayFase[i][5][j]).limit_denominator())
            auxArrayCxCj.append(aux1)

        for j in range(len(arrayFase[i][6])):
            aux1 = str(Fraction(arrayFase[i][6][j]).limit_denominator())
            auxArrayZjCj.append(aux1)
        
        auxResultadoZ = str(Fraction(arrayFase[i][7]).limit_denominator())

        auxTablaFase = []
        auxTablaFase = [auxArrayNombreVariables, auxArrayCx, auxArrayXb, auxArrayBi, auxArrayCj, auxArrayCxCj, auxArrayZjCj, auxResultadoZ]
        arrayFraccionesFase.append(auxTablaFase)
    return arrayFraccionesFase


@app.route('/metodoGrafico')
def metodoGrafico():
    return render_template("metodoGrafico.html")    

@app.route('/procesar', methods=['GET'])
def procesar():
    operacion = 0
    funcionObjetivoY = 0
    funcionObjetivoX = 0
    cantidadRestricciones = 0

    cantidadRestricciones = int(request.args.get("restricciones"))

    operacion = request.args.get("metodo")

    funcionObjetivoX = request.args.get("Xfo")
    funcionObjetivoX = round(pasarFraccionDecimal(funcionObjetivoX),6)

    funcionObjetivoY = request.args.get("Yfo")
    funcionObjetivoY = round(pasarFraccionDecimal(funcionObjetivoY),6)

    return render_template("restricciones.html", cantidadRestricciones=cantidadRestricciones, operacion=operacion,funcionObjetivoX=funcionObjetivoX, funcionObjetivoY=funcionObjetivoY)

@app.route('/realizarProceso',methods=['POST'])
def realizarProceso():
    cantidadRestricciones = int(request.form.get("cantidadRestricciones"))
    operacion = request.form.get("metodo")
    funcionObjetivoX = request.form.get("Xfo")
    funcionObjetivoY = request.form.get("Yfo")

    nombreImagen = 0
    arrayRestricciones = []
    arrayValorObjetivo = []
    arrayCategoriaFO = []
    arrayFracciones = []
    tMayor = 0

    arrayRestricciones = obtenerRestricciones(cantidadRestricciones)
    arrayTotalPuntos = obtenerPuntosCorte(arrayRestricciones)
    arrayPuntosGrafica, arrayValidarPuntosGrafica, arrayTotalPuntos, arrayPuntosNegativos, arrayCategoriaPunto = obtenerCoordenadas(arrayRestricciones, arrayTotalPuntos)
    arrayValorObjetivo, arrayCategoriaFO,tMayor = validarRestricciones(funcionObjetivoX, funcionObjetivoY, arrayRestricciones, arrayTotalPuntos)
    obtenerFuncionObjetivo(operacion, arrayValorObjetivo, arrayCategoriaFO)
    nombreImagen = mostrarGrafica(arrayCategoriaPunto, arrayPuntosGrafica, arrayValidarPuntosGrafica, arrayPuntosNegativos, arrayCategoriaFO, arrayValorObjetivo,tMayor)

    arrayFracciones = arrayValorObjetivo
    fraccionesArray = []
    aux1 = 0
    aux2 = 0
    aux3 = 0

    for i in range(len(arrayFracciones)):

        aux1 = str(Fraction(arrayFracciones[i][0]).limit_denominator())
        aux2 = str(Fraction(arrayFracciones[i][1]).limit_denominator())
        aux3 = str(Fraction(arrayFracciones[i][2]).limit_denominator())
        fraccionesArray.append([aux1, aux2, aux3])

    return render_template("grafica.html",nombreImagen=nombreImagen, arrayRestricciones=arrayRestricciones,
    funcionObjetivoX=funcionObjetivoX,funcionObjetivoY=funcionObjetivoY, operacion=operacion, arrayValorObjetivo=arrayValorObjetivo,
    arrayCategoriaFO=arrayCategoriaFO, fraccionesArray=fraccionesArray)

@app.route('/integrantes')
def integrantes():
    return render_template("integrantes.html")

if __name__ == '__main__':
    app.run(debug=True)