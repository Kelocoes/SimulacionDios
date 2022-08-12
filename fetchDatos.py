import pandas as pd

def infoCali():
    datosSalida=[]
    datosEntrada=[]
    datosSalida=pd.read_html(f'https://es.airports-worldwide.info/aeropuerto/CLO/salidas/Salidas_Cali_Alfonso_Bonillaaragon_airport_Cali_CLO_SKCL?time=2018-12-20%A300')
    datosEntrada=pd.read_html(f'https://es.airports-worldwide.info/aeropuerto/CLO/llegadas/_Cali_Alfonso_Bonillaaragon_airport_Cali_CLO_SKCL?time=2018-12-20%A300')
    llegadas=[]
    salidas=[]

    for tabla in datosEntrada:
            llegadas.extend(tabla['Llegada'])
    for tabla in datosSalida:
            salidas.extend(tabla['Partida'])

    salidas = Corregir(salidas)
    llegadas = Corregir(llegadas)

    #print(len(salidas),len(llegadas))
    with open('cali_llegadas.txt', 'w') as sal :
        sal.write(' '.join(llegadas))

    with open('cali_salidas.txt', 'w') as sal :
        sal.write(' '.join(salidas))
    return [salidas,llegadas]

    
def infoMx():
    datosSalida=[]
    datosEntrada=[]
    
    datosSalida=pd.read_html(f'https://es.airports-worldwide.info/aeropuerto/MTY/salidas/Salidas_Aeropuerto_Internacional_Mariano_Escobedo?time=2018-12-20%A300')
    datosEntrada=pd.read_html(f'https://es.airports-worldwide.info/aeropuerto/MTY/llegadas/Llegadas_Aeropuerto_Internacional_Mariano_Escobedo?time=2018-12-20%A300')

    llegadas=[]
    salidas=[]

    for tabla in datosEntrada:
        llegadas.extend(tabla['Llegada'])
    
    for tabla in datosSalida:
        salidas.extend(tabla['Partida'])

    llegadas = Corregir(llegadas)
    salidas = Corregir(salidas)
    with open('mx_llegadas.txt', 'w') as sal :
        sal.write(' '.join(llegadas))

    with open('mx_salidas.txt', 'w') as sal :
        sal.write(' '.join(salidas))

    return [salidas,llegadas]

def Corregir(arreglo):
    for i in range(len(arreglo)):
        if len(arreglo[i]) != 5:
            segundo = arreglo[i][5:len(arreglo[i])]
            arreglo[i] = segundo
    return arreglo
