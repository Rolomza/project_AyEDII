from uber import *

#Determina los vehiculos más cercanos a una persona
def create_trip(map,person,location):

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
        for car in map_cars_key:
            if map_elements[car]['amount'] > map_elements[person]['amount']:
                map_cars.pop(car)
        
        #A los vehiculos restantes les obtengo su vertice referencia
        cars_ref = [] #Almacenara tuplas (vehiculos,vertices)
        for car in map_cars_key:
            car_vertexpair = [map_elements[car]['address'][0][0],map_elements[car]['address'][1][0]]
            cars_ref.append((car,car_vertex_ref(map_elements,car,car_vertexpair)))
        #print(cars_ref)

        path_matrix = read_from_disk('path_matrix_serialized.bin') #Leo de memoria la matriz de caminos
        #print(person_vertex)
        #Veo las distancias de los caminos correspondientes a la referencia de los autos
        distance_list = []
        for v in cars_ref:
            v.append(path_matrix[person_vertex-1][v[1]-1])
        print(cars_ref)
        #print(path_matrix[9])


    except:
        print(f'not person {person} in map')


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