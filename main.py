import Bondad as bd
import numpy as np
import statistics # Aspecto para generar estadisticas
import random ## Aspecto aleatorio
import simpy
import math
import matplotlib.pyplot as plt

''''''
## Arreglos de graficos

datosx = [] ## tiempo
datosy = [] ## salida de aviones

''''''

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

mediaSalidaMx = statistics.mean(mx[0])
mediaLlegadaMx= statistics.mean(mx[1])

varianzaSalidaMx = statistics.variance(mx[0], mediaSalidaMx)
varianzaLlegadaMx = statistics.variance(mx[1], mediaLlegadaMx)


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
            #print("El avion " + str(avion) + " se retraso " + str(round(minutos,0)) + " minutos")
        if (llegada):
            yield self.env.timeout(20,46)
            yield self.env.timeout(abs(random.normalvariate(self.mediaAirSalida, self.varAirSalida)*self.largoSalida))
        else:
            yield self.env.timeout(abs(random.normalvariate(self.mediaAirSalida, self.varAirSalida)*self.largoSalida))

        yield self.env.timeout(15,21)
    


#Proceso que tienen que realizar
def aterrizadoYDespegue(env, avion, llegada, aeropuerto):
    
    tiempo_llegada = env.now
    #print("El avion " + str(avion) + " llego con tiempo " + str(round(tiempo_llegada,0)) + " minutos")

    with aeropuerto.parqueaderos.request() as peticion:
        yield peticion
        yield env.process(aeropuerto.ocupar_parqueo(avion, llegada))

    #print("El avion " + str(avion) + " salio con tiempo " + str(round(env.now,0)) + " minutos")
    holi[0] = holi[0] - 1
    #print("> Tiempo total del avion " + str(avion) + " en el aeropuerto fue de " + str(round((env.now-tiempo_llegada),0)) + " minutos")
    tiempo_espera.append(env.now - tiempo_llegada)

def correr_aeropuerto(env, cant_parqueaderos, largoLlegada, largoSalida, mediaAirLlegada, mediaAirSalida, varAirLlegada, varAirSalida, probRetraso):

    aeropuerto = Aeropuerto(env, cant_parqueaderos, mediaAirSalida, varAirSalida, largoSalida, probRetraso)

    for avion in range(3):
        with aeropuerto.parqueaderos.request() as peticion:
            yield peticion
            yield env.process(aeropuerto.ocupar_parqueo(avion, False))
        #print("El avion " + str(avion) + " salio con tiempo " + str(round(env.now,0)) + " minutos")

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

""""""""""""""""""""""""""""""""""""""""""""""""
## grafico 

def graph(datosx, datosy, xlabel, ylabel, titulo):
    plt.plot(datosx, datosy, '-ok')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(titulo)

    plt.show()

""""""""""""""""""""""""""""""""""""""""""""""""

def main(): 
    
    # configuracion
    
    y1 = []
    y2 = []
    x = [1,2,3,4,5,6,7,8]
    for portones in range(8,0,-1):
        resul = []
        resul2 = []    
        
        for i in range(100):
            
            holi [0] = 0
            random.seed()
            # Correr:
            ##print("*** Probando el flujo de aviones de Cali en el aeropuerto de Cali ***")
            env = simpy.Environment()
            probRetraso = 0.05
            largoLlegada = len(cali[1])
            largoSalida = len(cali[0])

            env.process(correr_aeropuerto(env, portones, largoLlegada, largoSalida, mediaLlegadaCali, mediaSalidaCali, varianzaLlegadaCali, varianzaSalidaCali, probRetraso))
            env.run(until = 3600) ## Tiempo limite de la simulacion

            ## Visualizar resultados: 
            mins, secs = obtener_promedio_tiempo_espera(tiempo_espera)
            #print(
            #    "Corriendo la simulacion...",
            #    f"\nEl tiempo de espera promedio fue de {mins} minutos y  {secs} segundos.",
            #    )

            #print("Numero de aviones en espera para salir restantes: " + str(holi[0]))
            resul.append(mins)
            resul2.append(holi[0])
        y1.append(statistics.mean(resul))
        y2.append(statistics.mean(resul2))
    print(y1)
    print(y2)
    
    graph(x, y1[::-1], 'Número de portones', 'Tiempo de espera' , 'Grafico 1')
    graph(x, y2[::-1], 'Numero de portones', 'Aviones en espera', 'Grafico 2')


    """
    y1 = []
    y2 = []
    x = [1,2,3,4,5,6,7,8]
    for portones in range(8,0,-1):
        resul = []
        resul2 = []    
        
        for i in range(100):
            
            holi [0] = 0
            random.seed()
            # Correr:
            ##print("*** Probando el flujo de aviones de Monterrey en el aeropuerto de monterrey ***")
            env = simpy.Environment()
            probRetraso = 0.05
            largoLlegada = len(mx[1])
            largoSalida = len(mx[0])

            env.process(correr_aeropuerto(env, portones, largoLlegada, largoSalida, mediaLlegadaMx, mediaSalidaMx, varianzaLlegadaMx, varianzaSalidaMx, probRetraso))
            env.run(until = 3600) ## Tiempo limite de la simulacion

            ## Visualizar resultados: 
            mins, secs = obtener_promedio_tiempo_espera(tiempo_espera)
            #print(
            #    "Corriendo la simulacion...",
            #    f"\nEl tiempo de espera promedio fue de {mins} minutos y  {secs} segundos.",
            #    )

            #print("Numero de aviones en espera para salir restantes: " + str(holi[0]))
            resul.append(mins)
            resul2.append(holi[0])
        y1.append(statistics.mean(resul))
        y2.append(statistics.mean(resul2))
    print(y1)
    print(y2)
    
    graph(x, y1[::-1], 'Número de portones', 'Tiempo de espera' , 'Grafico 1')
    graph(x, y2[::-1], 'Numero de portones', 'Aviones en espera', 'Grafico 2')

    

        ### Probando el flujo de aviones de monterrey en Cali 
    resul = []
    resul2 = []
    for i in range(100):
        holi [0] = 0
        random.seed(i)
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
        
        print("Numero de aviones en espera para salir restantes: " + str(holi[0]))
        resul.append(mins)
        resul2.append(holi[0])
    print("Promedio de minutos de espera" + str(statistics.mean(resul)))   
    print("Promedio de aviones en espera" + str(statistics.mean(resul2)))
    """

if __name__ == '__main__':
    main()

