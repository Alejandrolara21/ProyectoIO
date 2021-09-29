from flask import Flask, render_template, request
from matplotlib import pyplot as plt

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
            mensaje,arrayTablasFase2 = fase2Maximizacion(resultadoZ,arrayUltimaTablaFase1,arrayXb,arrayBi,arrayFO,cantidadVariables,filas)
        elif(operacion == 2):
            #Minimizacion
            #FASE 2
            mensaje,arrayTablasFase2 = fase2Minimizacion(resultadoZ,arrayUltimaTablaFase1,arrayXb,arrayBi,arrayFO,cantidadVariables,filas)
    else:
        #FASE 1
        if(operacion ==1):
            #Maximizacion
            contArrayZjCJPositivos = validarZjCjMaximizacion(arrayZjCj)
            arrayUltimaTablaFase1,arrayTablasFase1,arrayNombreVariables,arrayCx,arrayXb,arrayBi,arrayCj,arrayCxCj,arrayZjCj,resultadoZ = fase1Maximizacion(contArrayZjCJPositivos,posTablaFase1,arrayBi,arrayCx,arrayZjCj,arrayCj,arrayNombreVariables,arrayTablasFase1,filas,columnaFase1)
            #FASE 2
            mensaje,arrayTablasFase2 = fase2Maximizacion(resultadoZ,arrayUltimaTablaFase1,arrayXb,arrayBi,arrayFO,cantidadVariables,filas)
        elif(operacion == 2):
            #Minimizacion
            #validar si hay puntos positivos en el arreglo ZjCj
            contArrayZjCJPositivos = validarZjCjMinimizacion(arrayZjCj)
            arrayUltimaTablaFase1,arrayTablasFase1,arrayNombreVariables,arrayCx,arrayXb,arrayBi,arrayCj,arrayCxCj,arrayZjCj,resultadoZ = fase1Minimizacion(contArrayZjCJPositivos,posTablaFase1,arrayBi,arrayCx,arrayZjCj,arrayCj,arrayNombreVariables,arrayTablasFase1,filas,columnaFase1)
            #FASE 2
            mensaje,arrayTablasFase2 = fase2Minimizacion(resultadoZ,arrayUltimaTablaFase1,arrayXb,arrayBi,arrayFO,cantidadVariables,filas)

    return render_template("dosFases.html",arrayTablasFase1=arrayTablasFase1,arrayTablasFase2=arrayTablasFase2,mensaje=mensaje,arrayFO=arrayFO)

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