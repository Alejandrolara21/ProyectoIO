from flask import Flask, render_template, request
from matplotlib import pyplot as plt

plt.switch_backend('agg')

from MetodoGrafico import *
from MetodoSimplex import *
app = Flask(__name__)

@app.route('/')
def home():
    if len(glob.glob("static/img/*.jpg")) > 5:
        for archivo in glob.glob("static/img/*.jpg"):
            try:
                remove(archivo)
            except OSError as e:
                print(f"Error:{e.strerror}")
                
    return render_template("index.html")

@app.route('/metodoGrafico')
def metodoGrafico():
    return render_template("metodoGrafico.html")    

@app.route('/metodoSimplex')
def metodoSimplex():
    return render_template("metodoSimplex.html")

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
    nombreImagenAnterior = 0
    tmayor = False
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