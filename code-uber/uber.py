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
    is_map_created = False
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
        vertices_objects_dict = instanciar_obj_vertices(sorted_vertices)

        # Creo mapa
        uber_map = Graph(vertices_objects_dict,edges_list)
        #uber_map.draw_graph()
        hacer_escritura(uber_map,'mapa_serializado.bin')
        print("Map created successfully")
        path = calculate_path(uber_map)
        hacer_escritura(path,'camino_serializado.bin')
        is_map_created = True
        return is_map_created
    except FileNotFoundError:
        print('Error: No such file or directory.')
        return is_map_created

def instanciar_obj_vertices(lista_elementos):
    dict_vertices = {}

    for i in range(len(lista_elementos)):
        dict_vertices[lista_elementos[i]] = Vertex(int(lista_elementos[i][1:]))
        #lista_vertices.append(Vertex(lista_elementos[i][1:]))
    
    return dict_vertices

# Funciones para serializar y guardar en disco

#Realiza la escritura de un objeto en un archivo local_path
def hacer_escritura(objeto,local_path):
    import pickle

    with open(local_path,'wb') as file:
        pickle.dump(objeto,file)

#Realiza la lectura de un objeto desde un archivo local_path
def hacer_lectura(local_path):
    import pickle

    with open(local_path,'br') as file:
        objeto = pickle.load(file)
    return objeto

# Los elementos fijos y moviles seran guardados en un diccionario de python

def load_fix_element(elements_map,name,address):

    # Asi como leo el mapa deberia tambien guardar en disco el diccionario de elementos?
    uber_map = hacer_lectura('mapa_serializado.bin')

    # Valido que no exista el elemento en el mapa
    if (check_name_validity(name)):
        if (name not in elements_map):
            parsed_address = parse_address_input(address)
            if (check_element_address(uber_map,parsed_address)):
                elements_map[name] = {'address': address}
                print("Fixed element loaded!")
            else:
                print('Not a valid address in map')
        else:
            print('The element already exists in map.')
    else:
        print('Not a valid name for a map element')
        

def load_movil_element(map,name,address,amount):
    print("Movil element loaded!")
    #map_elements[name] = {'address':address,'amount': amount}

def get_address(map,name):
    address = map[name]['address']
    return address

def at_same_location(map,name1,name2):
    if get_address(map,name1) == get_address(map,name2):
        return True
    else:
        return False

def check_name_validity(name):
    pattern = r'[HATSEKIPC]\d+'
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
    print("The street doesn't exist")
    return False

'''
create_map('mapa.txt')
uber_map = hacer_lectura('mapa_serializado.bin')
uber_map.draw_graph()
elements_map = {}
#address = "{<e2,5>,<e6,10>}"

address1 = [('e2',5),('e6',10)]

address_input = sys.argv[1]
print(address_input)
print(parse_address_input(address_input))

print(sys.argv)

try:
    is_map_created = False
    if(sys.argv[1] == "-create_map"):
        try:
            if (sys.argv[2] != ""):
                local_path = sys.argv[2]
                is_map_created = create_map(local_path)
        except IndexError:
            print("Local path not found. Insert -create_map <local_path>")

    if(sys.argv[1] == "-load_fix_element"):
        print('load fix function, is mapa created:', is_map_created)
        # if(is_map_created):
        #     if(sys.argv[1] == "-load_fix_element"):
        #         uber_map = hacer_lectura('mapa_serializado.bin')
        #         load_fix_element(uber_map,sys.argv[2],sys.argv[3])
    else:
        print("You must create a map first. Insert -create_map <local_path> to start.")

except IndexError:
    print("Insert -creat_map <local_path> to start.")
'''