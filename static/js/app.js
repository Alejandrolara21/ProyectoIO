document.addEventListener('DOMContentLoaded', function() {
    menuResponsive();
    validarInputs();
    fracciones();
});

function menuResponsive() {
    const menuResponsive = document.querySelector('.menu-mobile');
    menuResponsive.addEventListener('click', navegacionResponsive);
}

function navegacionResponsive() {
    const navegacion = document.querySelector('.navegacion');
    navegacion.classList.toggle('mostrar');
}


function validarInputs() {
    let inputs;
    if (document.querySelectorAll('INPUT')) {
        inputs = document.querySelectorAll('INPUT');
    }

    inputs.forEach((input) => {
        input.addEventListener('input', validarCaracteres);
    });

}

function validarCaracteres(e) {
    const arrayCaracteresValidos = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '/', '.', ',', '-'];
    const valorInput = e.target.value;
    const arrayValorInput = valorInput.split('');
    let cont = 0;
    let bandValFraccion = true;

    let contBarraDivision = 0;
    let bandBarraDivision = true;

    let bandValDivision = true;


    arrayValorInput.forEach((valor, indexInput) => {
        arrayCaracteresValidos.forEach((caracter) => {
            if (valor === caracter) {
                cont += 1;
            }
        });

        if (valor === '/' || valor === '.' || valor === ',') {
            bandValFraccion = validarFraccion(arrayValorInput, indexInput);
        }

        if (valor === '/') {
            contBarraDivision += 1;
        }
    });


    if (contBarraDivision === 1) {
        const arrayOperacionInput = valorInput.split('/');
        const numerador = isNaN(arrayOperacionInput[0]);
        const denominador = isNaN(arrayOperacionInput[1]);
        if (numerador || denominador || arrayOperacionInput[1] == 0) {
            bandValDivision = false;
        }
    }

    const alerta = document.querySelector('.alerta');
    const boton = document.querySelector('.boton');

    if (cont != valorInput.length || bandValFraccion === false || contBarraDivision > 1 || bandValDivision === false) {
        boton.setAttribute("disabled", "");
        alerta.classList.remove('hidden');

    } else {
        alerta.classList.add('hidden');
        boton.removeAttribute("disabled", "");
    }
}

function validarFraccion(array, index) {
    const arrayNumerosValidos = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];
    let contNum = 0;
    let band = true;
    arrayNumerosValidos.forEach(numero => {
        if (numero === array[index - 1]) {
            contNum += 1;
        }
        if (numero === array[index + 1]) {
            contNum += 1;
        }
    });
    if (contNum < 2) {
        band = false;
    }

    return band;
}

function fracciones() {
    const selectorBoton = document.querySelector('.boton-cambiar');
    const seleccionarSpanOcultar = document.querySelectorAll('.ocultar');
    const seleccionarSpanCambiar = document.querySelectorAll('.cambiar');
    const boton = document.getElementById("#cambiar");
    
    selectorBoton.addEventListener('click', (e) => {

        if (boton.textContent == 'Convertir a fraccion') {
            boton.textContent = "Convertir a enteros";

            seleccionarSpanCambiar.forEach(item => {
                item.classList.add('hidden');
            })

            seleccionarSpanOcultar.forEach(item => {
                item.classList.remove('hidden');
            })

        } else {

            boton.textContent = 'Convertir a fraccion'

            seleccionarSpanCambiar.forEach(item => {
                item.classList.remove('hidden');
            })

            seleccionarSpanOcultar.forEach(item => {
                item.classList.add('hidden');
            })

        }

    })

}
