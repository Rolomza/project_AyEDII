import re
#TODO Crear funcion que tome la direccion de llegada y recorra a traves de la variable parent hasta llegar a la posicion de salida
def dijkstra(G, s):
    s.distance = 0 #Init Relax
    Q = []
    Q.append(s)
    while len(Q) > 0:
        u = Q.pop(0)
        u.color = 'red'
        #Las listas de adyacencia son tuplas (Vertex, Weight)
        for v in G.adj_list[u.key-1]:
            if v[0].color != 'green':
                #Segundo caso, vertices ya visitados
                if v[0].distance != 'infinite':
                    if v[1] + u.distance < v[0].distance:
                        v[0].distance = v[1] + u.distance
                        v[0].parent = u
                else:
                    #Primer caso, vertice nunca antes visitado
                    v[0].distance = v[1] + u.distance
                    v[0].parent = u
                Q.append(v[0]) #Se añade a la lista por recorrer
        u.color = 'green'


def calculate_path(G):
    Discver_sorted = {k: v for k, v in sorted(G.vertices_list.items(), key=lambda x: [int(c) if c.isdigit() else c for c in re.split('(\d+)', x[0])])}
    print(Discver_sorted)
    verObj_list = list(Discver_sorted.values())
    #print(verObj_list)
    #Creo la matriz |V| x |V|
    dijkstraMatrix = [[] for _ in range(len(verObj_list))]

    #Recorro la lista de vertices y aplico dijktra
    for Avertex in verObj_list:

        dijkstra(G,Avertex)
        #Almaceno el estado del grafo después de dijkstra
        for Bvertex in verObj_list:
            dijkstraMatrix[Avertex.key-1].append((Bvertex.distance, Bvertex.parent))
        #printStatus(verObj_list)
        #print('=======')    
        #Reinicio el grafo
        resetGraph(verObj_list) 

    return dijkstraMatrix


#Devuelve los vertices a sus estados limpios
def resetGraph(verList):
    for vertex in verList:
        vertex.color = None
        vertex.parent = None
        vertex.distance = 'infinite'
        vertex.f = None

#Imprime el estado en el que se encuentra cada vertice
def printStatus(V):
    for i in range(len(V)):
        if V[i].parent != None:
            print(f'|v:{i+1}, d:{V[i].distance}, pi:{V[i].parent.key}| ')
        else:
            print(f'|v:{i+1}, d:{V[i].distance}, pi:{V[i].parent}| ')


