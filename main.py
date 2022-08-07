import fetchDatos as fD
import Bondad as bd
import scipy.stats as stats
import numpy as np
import PruebaCorridas as pc
from statistics import median

def PasarSegundos(hora):
    horas = hora.split(":")
    return 3600*int(horas[0]) + int(horas[1])*60

def NormalizarMedia(datos): 
    datos_normalizados = []
    maximo = max(datos)
    minimo = min(datos)
    for dato in datos:
        datos_normalizados.append((dato - minimo) /(maximo - minimo))
    return datos_normalizados
    
def Media(datos):
    val = 0
    for dato in datos:
        val += dato
    return val/len(datos)

def Varianza(datos, media):
    val = 0
    for dato in datos:
        val += (dato - media)**2
    return val/len(datos)    

## Obtenemos los datos:
## Primera lista de salida
## Segunda de llegada

cali = [[],[]]
mx = [[],[]]

with open('./cali_salidas.txt', 'r') as sal :
       lin = sal.read().split(' ')
       cali[0] = lin
with open('./cali_llegadas.txt', 'r') as sal :
       lin = sal.read().split(' ')
       cali[1] = lin

with open('./mx_salidas.txt', 'r') as sal :
       lin = sal.read().split(' ')
       mx[0] = lin 
with open('./mx_llegadas.txt', 'r') as sal :
       lin = sal.read().split(' ')
       mx[1] = lin 


cali[0] = [PasarSegundos(hora) for hora in cali[0]]
cali[1] = [PasarSegundos(hora) for hora in cali[1]]

cali[0] = NormalizarMedia(cali[0])
cali[1] = NormalizarMedia(cali[1])


mediaSalidaCali = Media(cali[0])
mediaLlegadaCali = Media(cali[1])

varianzaSalidaCali =  Varianza(cali[0],mediaSalidaCali)
varianzaLlegadaCali = Varianza(cali[1],mediaLlegadaCali)


## Prueba de chicuadrado cali
print("Chi salidas Cali")
bd.chiCuadradoTabla(cali[0], 0.05)
print("Llegadas Cali")
bd.chiCuadradoTabla(cali[1], 0.05)


mx[0] = [PasarSegundos(hora) for hora in mx[0]]
mx[1] = [PasarSegundos(hora) for hora in mx[1]]   

mx[0] = NormalizarMedia(mx[0])
mx[1] = NormalizarMedia(mx[1])

mediaSalidaMx = Media(mx[0])
mediaLlegadaMx= Media(mx[1])

varianzaSalidaMx = Varianza(mx[0], mediaSalidaMx)
varianzaLlegadaMx = Varianza(mx[1], mediaLlegadaMx)


## Prueba de chicuadrado Mexico - Monterrey
print("Chi salidas Mexico  monterey")
bd.chiCuadradoTabla(mx[0], 0.05)
print("Chi Llegadas Mexico - monterey")
bd.chiCuadradoTabla(mx[1], 0.05)

"""
## Pruebas de independencia por medio de la prueba de corridas
## Cali
print("Prueba de independencia de salidas Cali")
pc.runsTest(cali[0], median(cali[0]))
print("Prueba de independencia de entradas Cali")
pc.runsTest(cali[1], median(cali[1]))
## Mexico
print("Prueba de independencia de salidas Mexico")
pc.runsTest(mx[0], median(mx[0]))
print("Prueba de independencia de llegadas Mexico")
pc.runsTest(mx[1], median(mx[1]))
"""
