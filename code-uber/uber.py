import sys
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
                if amount >= 0:
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

'''
create_map('mapa.txt')
uber_map = read_from_disk('map_serialized.bin')
uber_map.draw_graph()
address_input = "<e8,20> <e10,30>"

# load_fix_element("H1", "<e8,20> <e10,30>")
# load_movil_element("P1", "<e8,10> <e10,40>", 2000)
# map_elements = read_from_disk('map_elements_serialized.bin')
# print(map_elements)


# load_movil_element(map_elements,'C1',"<e2,20> <e6,30>",2000)
# print(map_elements)

# print(sys.argv)

# try:
#     is_map_created = False
#     if(sys.argv[1] == "-create_map"):
#         try:
#             if (sys.argv[2] != ""):
#                 local_path = sys.argv[2]
#                 is_map_created = create_map(local_path)
#         except IndexError:
#             print("Local path not found. Insert -create_map <local_path>")

#     if(sys.argv[1] == "-load_fix_element"):
#         print('load fix function, is mapa created:', is_map_created)
#         # if(is_map_created):
#         #     if(sys.argv[1] == "-load_fix_element"):
#         #         uber_map = hacer_lectura('mapa_serializado.bin')
#         #         load_fix_element(uber_map,sys.argv[2],sys.argv[3])
#     else:
#         print("You must create a map first. Insert -create_map <local_path> to start.")

# except IndexError:
#     print("Insert -creat_map <local_path> to start.")
'''