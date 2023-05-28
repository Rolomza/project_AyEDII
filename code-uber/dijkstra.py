

#TODO Crear funcion que tome la direccion de llegada y recorra a traves de la variable parent hasta llegar a la posicion de salida
def dijkstra(G, s):
    initRelax(G, s)
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





#Establece todos los vertices excepto s con distancia(d) infinito y sin predecesor(pi)
#s poseera distancia(d) 0
def initRelax(G,s):
    for vertex in G.vertices_list:
        if vertex == s:
            vertex.distance = 0
        else:
            vertex.distance = 'infinite'

#Devuelve los vertices a sus estados limpios
def resetGraph(G):
    for vertex in G.vertices_list:
        vertex.color = None
        vertex.parent = None
        vertex.distance = None
        vertex.f = None

#Imprime el estado en el que se encuentra cada vertice
def printStatus(V):
    for i in range(len(V)):
        if V[i].parent != None:
            print(f'|v:{i+1}, d:{V[i].distance}, pi:{V[i].parent.key}| ')
        else:
            print(f'|v:{i+1}, d:{V[i].distance}, pi:{V[i].parent}| ')