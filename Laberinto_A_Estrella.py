# Viaje por carretera con búsqueda A*
import functools
from Arbol_Nodo import Nodo
import serial,time

def compara(x, y):
    lat1=coord[x.get_datos()][0]
    lon1=coord[x.get_datos()][1]
    lat2=coord[solucion][0]
    lon2=coord[solucion][1]
    d=int(geodist_lat(lat1,lat2)+geodist_lon(lon1,lon2))
    c1=x.get_coste()+d
    
    lat1=coord[y.get_datos()][0]
    lon1=coord[y.get_datos()][1]
    lat2=coord[solucion][0]
    lon2=coord[solucion][1]
    d=int(geodist_lat(lat1,lat2)+geodist_lon(lon1,lon2))
    c2=y.get_coste()+d
    
    return c1-c2

def geodist_lat(lat1,lat2):
    latitud = lat1-lat2
    return latitud

def geodist_lon(lon1,lon2):
    longitud = lon1-lon2
    return longitud

def buscar_solucion_UCS(conexiones, estado_inicial, solucion):
    solucionado=False
    nodos_visitados=[]
    nodos_frontera=[]
    nodo_inicial = Nodo(estado_inicial)
    nodo_inicial.set_coste(0)
    nodos_frontera.append(nodo_inicial)
    while (not solucionado) and len(nodos_frontera)!=0:
        # ordenar la lista de nodos frontera
        nodos_frontera = sorted(nodos_frontera, key=functools.cmp_to_key(compara))
        nodo=nodos_frontera[0]
        # extraer nodo y añadirlo a visitados
        nodos_visitados.append(nodos_frontera.pop(0))
        if nodo.get_datos() == solucion:
            # solución encontrada
            solucionado=True
            return nodo
        else:
            # expandir nodos hijo (ciudades con conexión)
            dato_nodo = nodo.get_datos()
            lista_hijos=[]
            for un_hijo in conexiones[dato_nodo]:
                hijo=Nodo(un_hijo)
                # cálculo g(n): coste acumulado
                coste = conexiones[dato_nodo][un_hijo]
                hijo.set_coste(nodo.get_coste() + coste)
                lista_hijos.append(hijo)
                if not hijo.en_lista(nodos_visitados):
                    # si está en la lista lo sustituimos con
                    # el nuevo valor de coste si es menor
                    if hijo.en_lista(nodos_frontera):
                        for n in nodos_frontera:
                            if n.igual(hijo) and n.get_coste()>hijo.get_coste():
                                nodos_frontera.remove(n)
                                nodos_frontera.append(hijo)
                    else :
                        nodos_frontera.append(hijo)
            
            nodo.set_hijos(lista_hijos)

if __name__ == "__main__":
# 1=Derecha
# 2=Adelante
# 3=Izquierda
# 4=Atras
    conexiones = {
        '1':{'2':1},
        '2':{'1':3,'8':2,'3':1},
        '3':{'2':3,'4':1},
        '4':{'3':3,'5':1},
        '5':{'4':3,'11':2,'6':1},
        '6':{'5':3},
        '7':{'13':2,'8':1},
        '8':{'7':3,'14':2,'9':1,'2':4},
        '9':{'8':3,'15':2,'10':1},
        '10':{'9':3,'16':2,'11':1},
        '11':{'10':3,'12':1,'5':4},
        '12':{'11':3},
        '13':{'19':2,'7':4},
        '14':{'20':2,'8':4},
        '15':{'21':2,'9':4},
        '16':{'17':1,'10':4},
        '17':{'16':3,'18':1},
        '18':{'17':3,'24':2,},
        '19':{'25':2,'13':4},
        '20':{'14':4},
        '21':{'22':1,'15':4},
        '22':{'21':3,'28':2,'23':1},
        '23':{'22':3,'24':1},
        '24':{'23':3,'18':4},
        '25':{'26':1,'19':4},
        '26':{'25':3,'27':1},
        '27':{'26':3,'28':1},
        '28':{'27':3,'29':1,'22':4},
        '29':{'28':3,'30':1},
        '30':{'29':3}
    }

    coord = {
            '1':(1, 1),
            '2':(1, 2),
            '3':(1, 3),
            '4':(1, 4),
            '5':(1, 5),
            '6':(1, 6),
            '7':(2, 1),
            '8':(2, 2),
            '9':(2, 3),
            '10':(2, 4),
            '11':(2, 5),
            '12':(2, 6),
            '13':(3, 1),
            '14':(3, 2),
            '15':(3, 3),
            '16':(3, 4),
            '17':(3, 5),
            '18':(3, 6),
            '19':(4, 1),
            '20':(4, 2),
            '21':(4, 3),
            '22':(4, 4),
            '23':(4, 5),
            '24':(4, 6),
            '25':(5, 1),
            '26':(5, 1),
            '27':(5, 3),
            '28':(5, 4),
            '29':(5, 5),
            '30':(5, 6)
            }
    
    serialArduino = serial.Serial(port='COM3',baudrate=9600,timeout=0)
    estado_inicial='1'
    solucion='30'
    nodo_solucion = buscar_solucion_UCS(conexiones, estado_inicial, solucion)
    # mostrar resultado
    resultado=[]
    nodo=nodo_solucion
    while nodo.get_padre() != None:
        resultado.append(nodo.get_datos())
        nodo = nodo.get_padre()
    resultado.append(estado_inicial)
    resultado.reverse()

    print(resultado)
    resultado.append(0)
    
    for m in range(len(resultado)):
        resultado[m] = int(resultado[m])

    for i in range(len(resultado)):
        time.sleep(2)
        print(serialArduino.read())
        if resultado[i] != 0:
            if resultado[i+1] == resultado[i]+1:
                serialArduino.write('1'.encode('utf-8'))
            elif resultado[i+1] == resultado[i]+6:
                serialArduino.write('2'.encode('utf-8'))
            elif resultado[i+1] == resultado[i]-1:
                serialArduino.write('3'.encode('utf-8'))
        else:
            print("Finalizado")