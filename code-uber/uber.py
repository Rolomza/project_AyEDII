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
            edge_u = edges_list[i][0]
            edge_v = edges_list[i][1]
            weight = edges_list[i][2]
            self.adj_list[edge_u.key - 1].append((edge_v,weight))
            #self.adj_list[edges_list[i][1].key - 1].append(edges_list[i][0])
    
    def draw_graph(self):
        for i in range(len(self.adj_list)):
            print('|',i+1,'|-->',end="")
            for vertex in self.adj_list[i]:
                print('|',vertex[0].key,'(w:',vertex[1],')|',end="")
            print()


def create_map(local_path):

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
        
        print(vertices)
        print(edges_list)


def crear_dict_vertices(lista_elementos):
    lista_vertices = {}

    for elemento in lista_elementos:
        lista_vertices[elemento] = Vertex(elemento[1:])
    
    return lista_vertices

create_map("mapa.txt")






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





