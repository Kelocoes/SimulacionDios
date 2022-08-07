import numpy
import matplotlib.pyplot as plt
import math
from tabulate import tabulate


def frecuenciasEsperadas(numero_datos, numero_clases):
    frec_esperada = numero_datos/numero_clases
    frecuenciaEperada = []
    for i in range(numero_clases):
        frecuenciaEperada.append(frec_esperada)
    return frecuenciaEperada

def crearClases(clases):
    longitud_intervalo = 1/clases
    intervalos = []
    for i in range(clases):
        intervalos.append([longitud_intervalo*i, longitud_intervalo*(i+1)])
    return intervalos

def frecuenciaObservada(limiteInferior, limiteSuperior, datos):
    frecuencia = 0
    for dato in datos:
        if(dato > limiteInferior and dato <= limiteSuperior):
            frecuencia += 1
    return frecuencia

def frecuenciasObservadas(intervalos, datos):
    frecuencias = []
    for intervalo in intervalos:
        frecuencias.append(frecuenciaObservada(intervalo[0], intervalo[1], datos))
    return frecuencias

def valorCalculadoChiCuadrado(FE, FO):
    return ((FE - FO)**2)/FE


def pruebaChiCuadrado(datos, confianza):
    n = len(datos)
    #print(n)
    c = math.ceil(math.sqrt(n))
    gl = c - 1
    intervalo_clases = crearClases(c)
    FE = frecuenciasEsperadas(n, c)
    FO = frecuenciasObservadas(intervalo_clases, datos)

    #print(n)
    #print(c)
    #print(gl)
    #print(intervalo_clases)
    #print(FE)
    #print(FO)

    chiCuadrados = [valorCalculadoChiCuadrado(int(FE[i]), int(FO[i])) for i in range(len(FE))]
    x2calc = sum(chiCuadrados)

    datostabla = {
                    0.05 : {
                        1: 3.841,
                        2: 5.991,
                        3: 7.815,
                        4: 9.488,
                        5: 11.070,
                        6: 12.592,
                        7: 14.067,
                        8: 15.507,
                        9: 16.919,
                        10: 18.307,
                        11: 19.675,
                        12: 21.026,
                        13: 22.362,
                        14: 23.685,
                        15: 24.996,
                        16: 26.296,
                        17: 27.587,
                        18: 28.869,
                        19: 30.144,
                        20: 31.410,
                        21: 32.671
                    }
                }

    x2crit = datostabla[confianza][gl]
    pasaONo = x2calc <= x2crit

    tablaResultados = []
    for fila in zip(intervalo_clases,FO, FE, chiCuadrados):
        tablaResultados.append(fila)
    return  [tablaResultados, x2calc, x2crit, pasaONo]


def chiCuadradoTabla(datos, confianza):
    res = pruebaChiCuadrado(datos, confianza)
    print("x2calc = " + str(res[1]))
    print("x2crit = " + str(res[2]))

    if(res[3]):
        print("El generador es bueno en cuanto a uniformidad pues el valor calculado es menor o igual al critico")
    else:
        print("El generador no es bueno en cuanto a uniformidad pues el valor calculado es mayor al critico")
    cabecera = ["Intervalo Clase", "FO", "FE", "(FE-FO)^2/FE"]
    print(tabulate(res[0], cabecera, tablefmt="grid"))
    return res[3]


#print(pruebaChiCuadrado([0.1,0.2,0.3,0.1], 0.05))

#chiCuadradoTabla([0.1,0.2,0.3,0.1], 0.05)


