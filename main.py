import fetchDatos as fD
import Bondad as bd
import scipy.stats as stats
import numpy as np
import PruebaCorridas as pc
import statistics # Aspecto para generar estadisticas
import random ## Aspecto aleatorio
import simpy
import math
"""FASE DE PRUEBAS DE BONDAD"""

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


mediaSalidaCali = statistics.mean(cali[0])
mediaLlegadaCali = statistics.mean(cali[1])

varianzaSalidaCali =  statistics.variance(cali[0],mediaSalidaCali)
varianzaLlegadaCali = statistics.variance(cali[1],mediaLlegadaCali)
print(mediaLlegadaCali,varianzaLlegadaCali)

aux = 0
while (aux < 10):
    holi = random.normalvariate(mediaLlegadaCali, math.sqrt(varianzaLlegadaCali))*len(cali[1])
    holi2 = random.normalvariate(mediaSalidaCali, math.sqrt(varianzaSalidaCali))*len(cali[0])
    print(abs(holi),abs(holi2))
    aux += 1


## Prueba de chicuadrado cali
print("Chi salidas Cali")
bd.chiCuadradoTabla(cali[0], 0.05)
print("Llegadas Cali")
bd.chiCuadradoTabla(cali[1], 0.05)

mxSeg = [[],[]]

mxSeg[0] = [PasarSegundos(hora) for hora in mx[0]]
mxSeg[1] = [PasarSegundos(hora) for hora in mx[1]]   

mx[0] = NormalizarMedia(mxSeg[0])
mx[1] = NormalizarMedia(mxSeg[1])

mediaSalidaMx = Media(mx[0])
mediaLlegadaMx= Media(mx[1])

varianzaSalidaMx = Varianza(mx[0], mediaSalidaMx)
varianzaLlegadaMx = Varianza(mx[1], mediaLlegadaMx)


## Prueba de chicuadrado Mexico - Monterrey
print("Chi salidas Mexico  monterey")
bd.chiCuadradoTabla(mx[0], 0.05)
print("Chi Llegadas Mexico - monterey")
bd.chiCuadradoTabla(mx[1], 0.05)


tiempo_espera = []
holi = [0]

""""""""""""""""""""""""""""""""""""""""""""""""
## Simulacion

class Aeropuerto(object):

    def __init__(self, env, parqueaderos, mediaAirSalida, varAirSalida, largoSalida, probRetraso):
        self.env = env
        self.mediaAirSalida = mediaAirSalida
        self.varAirSalida = varAirSalida
        self.largoSalida = largoSalida
        self.parqueaderos = simpy.Resource(env, parqueaderos)
        self.probRetraso = probRetraso

    def ocupar_parqueo(self, avion, llegada):
        
        if(random.uniform(0,1) <= self.probRetraso):
            minutos = random.uniform(30, 80)
            yield self.env.timeout(minutos)
            print("El avion " + str(avion) + " se retraso " + str(round(minutos,0)) + " minutos")
        if (llegada):
            yield self.env.timeout(20,46)
            yield self.env.timeout(abs(random.normalvariate(self.mediaAirSalida, self.varAirSalida)*self.largoSalida))
        else:
            yield self.env.timeout(abs(random.normalvariate(self.mediaAirSalida, self.varAirSalida)*self.largoSalida))

        yield self.env.timeout(15,21)
    


#Proceso que tienen que realizar
def aterrizadoYDespegue(env, avion, llegada, aeropuerto):
    
    tiempo_llegada = env.now
    print("El avion " + str(avion) + " llego con tiempo " + str(round(tiempo_llegada,0)) + " minutos")

    with aeropuerto.parqueaderos.request() as peticion:
        yield peticion
        yield env.process(aeropuerto.ocupar_parqueo(avion, llegada))

    print("El avion " + str(avion) + " salio con tiempo " + str(round(env.now,0)) + " minutos")
    holi[0] = holi[0] - 1
    print("> Tiempo total del avion " + str(avion) + " en el aeropuerto fue de " + str(round((env.now-tiempo_llegada),0)) + " minutos")
    tiempo_espera.append(env.now - tiempo_llegada)

def correr_aeropuerto(env, cant_parqueaderos, largoLlegada, largoSalida, mediaAirLlegada, mediaAirSalida, varAirLlegada, varAirSalida, probRetraso):

    aeropuerto = Aeropuerto(env, cant_parqueaderos, mediaAirSalida, varAirSalida, largoSalida, probRetraso)

    for avion in range(3):
        with aeropuerto.parqueaderos.request() as peticion:
            yield peticion
            yield env.process(aeropuerto.ocupar_parqueo(avion, False))
        print("El avion " + str(avion) + " salio con tiempo " + str(round(env.now,0)) + " minutos")

    while True:
        yield env.timeout(abs(random.normalvariate(mediaAirLlegada, math.sqrt(varAirLlegada))*largoLlegada))
        holi[0] = holi[0] + 1
        avion += 1 
        env.process(aterrizadoYDespegue(env, avion, True, aeropuerto))
        

""""""""""""""""""""""""""""""""""""""""""""""""

def obtener_promedio_tiempo_espera(tiempo_espera):
    tiempo_promedio = statistics.mean(tiempo_espera)

    minutos, frac_minutos = divmod(tiempo_promedio, 1)
    segundos = frac_minutos * 60
    return round(minutos), round(segundos)
    
""""""""""""""""""""""""""""""""""""""""""""""""

def main(): 
    # configuracion
    
    random.seed(123)

    ## Correr:
    '''
    largoLlegada = len(cali[1])
    largoSalida = len(cali[0])
    probRetraso = 0.05
    env = simpy.Environment()
    env.process(correr_aeropuerto(env, 7, largoLlegada, largoSalida, mediaLlegadaCali, mediaSalidaCali, varianzaLlegadaCali, varianzaSalidaCali, probRetraso))
    env.run(until = 3600) ## Tiempo limite de la simulacion

    ## Visualizar resultados: 
    mins, secs = obtener_promedio_tiempo_espera(tiempo_espera)
    print(
        "Corriendo la simulacion...",
        f"\nEl tiempo de espera promedio fue de {mins} minutos y  {secs} segundos.",
        )

    
    ### Probando el flujo de aviones de monterrey en Cali 
    ## Correr: 
    print("*** Probando el flujo de aviones de Monterrey, mx en Cali  ***")
    largoLlegada = len(mx[1])
    largoSalida = len(mx[0])
    probRetraso = 0.05
    env = simpy.Environment()
    env.process(correr_aeropuerto(env, 7, largoLlegada, largoSalida, mediaLlegadaMx, mediaSalidaMx, varianzaLlegadaMx, varianzaSalidaMx, probRetraso))
    env.run(until = 3600) ## Tiempo limite de la simulacion

    ## Visualizar resultados: 
    mins, secs = obtener_promedio_tiempo_espera(tiempo_espera)
    print(
        "Corriendo la simulacion...",
        f"\nEl tiempo de espera promedio fue de {mins} minutos y  {secs} segundos.",
        )
    print(holi)
    '''

    # Correr:
    print("*** Probando el flujo de aviones de Monterrey en el aeropuerto de monterrey ***")
    env = simpy.Environment()
    probRetraso = 0.05
    largoLlegada = len(mx[1])
    largoSalida = len(mx[0])
    
    env.process(correr_aeropuerto(env, 8, largoLlegada, largoSalida, mediaLlegadaMx, mediaSalidaMx, varianzaLlegadaMx, varianzaSalidaMx, probRetraso))
    env.run(until = 3600) ## Tiempo limite de la simulacion

    ## Visualizar resultados: 
    mins, secs = obtener_promedio_tiempo_espera(tiempo_espera)
    print(
        "Corriendo la simulacion...",
        f"\nEl tiempo de espera promedio fue de {mins} minutos y  {secs} segundos.",
        )

    print("Numero de aviones en espera para salir restantes: " + str(holi[0]))

if __name__ == '__main__':
    main()

