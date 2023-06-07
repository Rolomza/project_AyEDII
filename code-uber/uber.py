import os
import re

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
    distance = None
    f = None

class Graph:
    # vertices_list = [v1,v2,v3,...,vn]
    # edges_list = [(v1,v2),(v2,v3),...,(vi,vj)]
    def __init__(self,vertices_list,edges_list):
        self.vertices_list = vertices_list
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
        vertices_objects_dict = instanciar_obj_vertices(sorted_vertices)

        # Creo mapa
        uber_map = Graph(vertices_objects_dict,edges_list)
        #uber_map.draw_graph()
        hacer_escritura(uber_map)
        print("Map created successfully")
    except FileNotFoundError:
        print('Error: No such file or directory ' + local_path)

def instanciar_obj_vertices(lista_elementos):
    dict_vertices = {}

    for i in range(len(lista_elementos)):
        dict_vertices[lista_elementos[i]] = Vertex(int(lista_elementos[i][1:]))
        #lista_vertices.append(Vertex(lista_elementos[i][1:]))
    
    return dict_vertices

# Funciones para serializar y guardar en disco

def hacer_escritura(objeto):
    import pickle

    with open('mapa_binario.bin','wb') as file:
        pickle.dump(objeto,file)

def hacer_lectura():
    import pickle

    with open('mapa_binario.bin','br') as file:
        objeto = pickle.load(file)
    return objeto


# Llamo la funcion para crear el mapa y guardarlo en disco a partir de un archivo de texto dado

create_map("./code-uber/mapa.txt")

# Cargo el mapa desde su serializacion en disco

mapa1 = hacer_lectura()


direcciones_mapa = {}

def add_location(map,name,address,amount):
    map[name] = {'address':address,'amount': amount}

def get_address(map,name):
    address = map[name]['address']
    return address

def at_same_location(map,name1,name2):
    if get_address(map,name1) == get_address(map,name2):
        return True
    return False





