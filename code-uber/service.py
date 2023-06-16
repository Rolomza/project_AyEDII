import sys
import os
import re
from dijkstra import calculate_path

# MAPA:
'''
Consiste de dos conjuntos <E,C>. E es un conjunto de esquinas {e1,e2,e3, ….} y C las calles que conectan dichas esquinas.
C es un conjunto de ternas ordenadas {<e1,e2,c>,<e3,e4,c>, <e2,e1,c>} que expresa la dirección y el largo de las calles (c = distancia entre e1 y e2).
'''

# 1 - Representar esquinas y calles como un grafo dirigido y ponderado mediante listas de adyacencia.

class Vertex:
    def __init__(self,key):
        self.key = key
    color = None
    parent = None
    distance = 'infinite'
    f = None

class Graph:
    # vertices_list = [v1,v2,v3,...,vn]
    # edges_list = [(v1,v2),(v2,v3),...,(vi,vj)]
    def __init__(self,vertices_list,edges_list):
        # {'e1': memory_element_e1, 'e2': memory_element_e2....}
        self.vertices_list = vertices_list
        # [['e1','e2',100],['e3','e4',150],...]
        self.edges_list = edges_list
    
        self.adj_list = [[] for _ in range(len(self.vertices_list))]
        
        for i in range(len(edges_list)):
            vertex_u = self.vertices_list[edges_list[i][0]]
            vertex_v = self.vertices_list[edges_list[i][1]]
            weight_u_v = int(edges_list[i][2])
            self.adj_list[vertex_u.key - 1].append((vertex_v,weight_u_v))
    
    def draw_graph(self):
        for i in range(len(self.adj_list)):
            print('|',i+1,'|-->',end="")
            for vertex in self.adj_list[i]:
                print('|',vertex[0].key,'(w:',vertex[1],')|',end="")
            print()


def create_map(local_path):
    try:
        with open(local_path) as file:
            # Read the vertices line
            vertices_line = file.readline().strip()
            # Extract the vertices from the first line
            vertices = vertices_line.split("=")[1].strip().strip("{}").split(",")

            # Read the edges line
            edges_line = file.readline().strip()
            # Extract the vertices from the second line
            edges_string = edges_line.split("=")[1].strip().strip("{}")
            # Regex edges expression
            edges_string_regexed = re.findall(r'<(.*?)>', edges_string)
        
        edges_list = []
        for edge in edges_string_regexed:
            edges_list.append(edge.split(","))
        # Ordeno vertices
        sorted_vertices = sorted(vertices)
        # Creo dict de objetos vertex
        vertices_objects_dict = instantiate_vertex_objects(sorted_vertices)

        # Creo mapa
        uber_map = Graph(vertices_objects_dict,edges_list)
        write_to_disk(uber_map,'map')

        # Creo diccionario para los elementos del mapa
        map_elements = {}
        write_to_disk(map_elements,'map_elements')

        path_matrix = calculate_path(uber_map)
        write_to_disk(path_matrix,'path_matrix')

        print("Map created successfully")
        
    except FileNotFoundError:
        print('Error: No such file or directory.')

def instantiate_vertex_objects(elements_list):
    dict_vertices = {}

    for i in range(len(elements_list)):
        dict_vertices[elements_list[i]] = Vertex(int(elements_list[i][1:]))
    
    return dict_vertices

# Functions for writing to and reading from disk

def write_to_disk(data, objectType):
    import pickle
    file_name = objectType + '_serialized.bin'
    with open(file_name,'wb') as file:
        pickle.dump(data,file)

def read_from_disk(local_path):
    import pickle
    with open(local_path,'br') as file:
        data = pickle.load(file)
    return data

# Los elementos fijos y moviles seran guardados en un diccionario de python

def load_fix_element(name,address):
    # Asi como leo el mapa deberia tambien guardar en disco el diccionario de elementos?
    uber_map = read_from_disk('map_serialized.bin')
    map_elements = read_from_disk('map_elements_serialized.bin')
    # Valido que no exista el elemento en el mapa
    if (check_name_validity(name,'fixed')):
        if (name not in map_elements):
            parsed_address = parse_address_input(address)
            if (check_element_address(uber_map,parsed_address)):
                map_elements[name] = {'address': parsed_address}
                write_to_disk(map_elements,'map_elements')
                print(f"Fixed element {name} loaded with address: {address}")
            else:
                print('Not a valid address in map')
        else:
            print('The element already exists in map.')
    else:
        print('Not a valid name for a fixed map element')
        

def load_movil_element(name,address,amount):

    uber_map = read_from_disk('map_serialized.bin')
    map_elements = read_from_disk('map_elements_serialized.bin')
    
    if (check_name_validity(name,'movil')):
        if (name not in map_elements):
            parsed_address = parse_address_input(address)
            if (check_element_address(uber_map,parsed_address)):
                if (amount >= 0):
                    map_elements[name] = {'address': parsed_address, 'amount': amount}
                    write_to_disk(map_elements,'map_elements')
                    print(f"Movil element {name} with amount {amount} loaded with address {address} ")
                else:
                    print('The amount must be at least 0')
            else:
                print('Not a valid address in map')
        else:
            print('The element already exists in map.')
    else:
        print('Not a valid name for a movil map element')

def get_address(map,name):
    address = map[name]['address']
    return address

def at_same_location(map,name1,name2):
    if get_address(map,name1) == get_address(map,name2):
        return True
    else:
        return False

def check_name_validity(name,type):
    if (type == 'fixed'):
        pattern = r'[HATSEKI]\d+'
        valid_name = re.match(pattern,name)
    if (type == 'movil'):
        pattern = r'[PC]\d+'
        valid_name = re.match(pattern,name)
    
    if valid_name:
        return True
    else:
        return False

def parse_address_input(address_input):
    pattern = r"<(\w+),(\d+)>"
    matches = re.findall(pattern, address_input)
    result = [(match[0], int(match[1])) for match in matches]
    return result
    
def check_element_address(map,address):
    # Address in form [('ex',d1),('ey',d2)]
    vertex_u = map.vertices_list[address[0][0]]
    vertex_v = map.vertices_list[address[1][0]]

    for element in map.adj_list[vertex_u.key - 1]:
        vertex = element[0]
        if (vertex == vertex_v):
            return True
    
    for element in map.adj_list[vertex_v.key - 1]:
        vertex = element[0]
        if (vertex == vertex_u):
            return True
        
    print("There is no street connecting these corners.")
    return False

# Creacion de viaje

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

            if len(location)>3:
                
                destiny_address = parse_address_input(location)
                uber_map = read_from_disk('map_serialized.bin')
                if check_element_address(uber_map,destiny_address):
                    virtual_location = 'destiny'
                    map_elements[virtual_location] = {'address':destiny_address}
                    write_to_disk(map_elements,'map_elemets')
                    location = virtual_location
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

        # 

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