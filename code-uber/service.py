from uber import *

#Determina los vehiculos más cercanos a una persona
def create_trip(person,location):

    map_elements = read_from_disk('map_elements_serialized.bin')

    #Determinar si la persona esta en el mapa
    #print(map_elements[person])
    try:
        pair_vertex = (map_elements[person]['address'][0][0],map_elements[person]['address'][1][0])
        person_vertex = person_vertex_ref(map_elements,person,pair_vertex) #Toma el vertice referente a la persona
        
        #filtro los vehiculos
        map_cars = {clave: valor for clave, valor in map_elements.items() if clave.startswith('C')} #Extraigo el diccionario de autos
        map_cars_key = list(map_cars.keys())
        #Elimina de la lista aquellos vehiculos que no se pueden pagar
        #for car in map_cars_key:
            #if map_elements[car]['amount'] > map_elements[person]['amount']:
                #map_cars.pop(car)
        
        #A los vehiculos restantes les obtengo su vertice referencia
        cars_ref = [] #Almacenara tuplas (vehiculos,vertices)
        for car in map_cars_key:
            car_vertexpair = (map_elements[car]['address'][0][0],map_elements[car]['address'][1][0])  
            cars_ref.append([car,car_vertex_ref(map_elements,car,car_vertexpair)])

        path_matrix = read_from_disk('path_matrix_serialized.bin') #Leo de memoria la matriz de caminos
        #Veo las distancias de los caminos correspondientes a la referencia de los autos
        valueperson_to_ref = calcule_ref(map_elements[person],person_vertex)
        for v in cars_ref:
            car_vertexpair = (map_elements[v[0]]['address'][0][0],map_elements[v[0]]['address'][1][0])
            valuecar_to_ref = calcule_ref(map_elements[v[0]], car_vertex_ref(map_elements,v[0],car_vertexpair))
            v.append(path_matrix[person_vertex-1][v[1]-1][0] + valuecar_to_ref + valueperson_to_ref)
        cars_ref = sorted(cars_ref, key=lambda x: x[2])

        payment = False
        #Devolucion de autos más cercanos
        #Calculo del costo
        for i in range(0,len(cars_ref)):
            costo = (cars_ref[i][2] + map_elements[cars_ref[i][0]]['amount'])/4
            if costo >= map_elements[person]['amount'] and i==0:
                print('No posee suficiente dinero para un viaje')
                break
            elif costo >= map_elements[person]['amount']:
                break
            elif i+1 == 4:
                break
            else:
                payment = True
                print(f"{i+1}.Auto {cars_ref[i][0]}: distancia {cars_ref[i][2]}, costo: {costo}")
        
        if payment:
            minpath = []
            pair_vertex = (map_elements[location]['address'][0][0],map_elements[location]['address'][1][0])
            location_vertex = person_vertex_ref(map_elements,location,pair_vertex)
            #print(location_vertex)
            #print(cars_ref)
            minpath.append(location_vertex)
            nextVertex = path_matrix[person_vertex-1][location_vertex-1][1]
            while nextVertex != None:
                minpath.append(nextVertex.key)
                nextVertex = path_matrix[person_vertex-1][nextVertex.key-1][1]
            print('Recorrido más corto para llegar a destino a través de las esquinas:')
            print(minpath)

    except:
        print(f'not person {person} in map')

def calcule_ref(element,reference):
    uber_map = read_from_disk('map_serialized.bin')

    if uber_map.vertices_list[element['address'][0][0]].key == reference:
        return  element['address'][0][1]
    elif uber_map.vertices_list[element['address'][1][0]].key == reference:
        return element['address'][1][1]
    

def person_vertex_ref(map_elements,person,pair_vertex):
    #Tomo el mapa de memoria
    uber_map = read_from_disk('map_serialized.bin')
    #uber_map.draw_graph()
    #Toma los pares de vertices referentes a la persona
    vertex1 = uber_map.vertices_list[pair_vertex[0]]
    vertex2 = uber_map.vertices_list[pair_vertex[1]]

    sense = ''
    for v in uber_map.adj_list[vertex1.key-1]:
        if v[0] == vertex2:
            sense = '12'
    for v in uber_map.adj_list[vertex2.key-1]:
        if v[0] == vertex1 and sense == '':
            sense = '21'
        elif v[0] == vertex1 and sense == '12':
            sense = 'd'
    
    #Si la calle es doble sentido, busco el camino mas corto
    if sense == 'd':
        if map_elements[person]['address'][0][1] <= map_elements[person]['address'][1][1]:
            return vertex1.key
        else:
            return vertex2.key
    #Si el sentido es de 1 hacia 2 devolvera el vertice 1
    elif sense == '12':
        return vertex1.key
    else:
        #Caso contrario devuelve el vertice 2
        return vertex2.key
    #print(vertex1.key, vertex2.key)
    #print(sense)

def car_vertex_ref(map_elements,car,pair_vertex):
    #Tomo el mapa de memoria
    uber_map = read_from_disk('map_serialized.bin')

    #Toma los pares de vertices referentes a la persona
    vertex1 = uber_map.vertices_list[pair_vertex[0]]
    vertex2 = uber_map.vertices_list[pair_vertex[1]]

    sense = ''
    for v in uber_map.adj_list[vertex1.key-1]:
        if v[0] == vertex2:
            sense = '12'
    for v in uber_map.adj_list[vertex2.key-1]:
        if v[0] == vertex1 and sense == '':
            sense = '21'
        elif v[0] == vertex1 and sense == '12':
            sense = 'd'
    
    #Si la calle es doble sentido, busco el camino mas corto
    if sense == 'd':
        if map_elements[car]['address'][0][1] <= map_elements[car]['address'][1][1]:
            return vertex1.key
        else:
            return vertex2.key
    #Si el sentido es de 1 hacia 2 devolvera el vertice 2
    elif sense == '12':
        return vertex2.key
    else:
        #Caso contrario devuelve el vertice 1
        return vertex1.key