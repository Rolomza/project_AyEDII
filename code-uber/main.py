from uber import create_map, hacer_lectura,Graph
from dijkstra import *

'''
#Prueba realizada por augusto cuando creo el mapa
e1 = Vertex(1)
e2 = Vertex(2)
e3 = Vertex(3)
e4 = Vertex(4)
e5 = Vertex(5)
e6 = Vertex(6)

esquinas = [e1,e2,e3,e4,e5,e6]

calles = [(e1,e2,100),(e1,e4,100),(e2,e5,50),(e3,e5,150),(e3,e6,100),(e4,e2,80),(e5,e4,120)]

mapa_uber = Graph(esquinas,calles)

mapa_uber.draw_graph()

e1 = Vertex(1)
e2 = Vertex(2)
e3 = Vertex(3)
e4 = Vertex(4)
e5 = Vertex(5)

#Prueba de dijkstra con ejemplo de diapositivas de teoria
esquinas = [e1,e2,e3,e4,e5]
calles = [(e1,e2,5),(e1,e3,10),(e2,e3,3),(e2,e4,2),(e2,e5,9),(e3,e2,2),(e3,e5,1),(e4,e1,7),(e4,e5,6),(e5,e4,4)]

mapa_uber = Graph(esquinas,calles)

mapa_uber.draw_graph()

'''
create_map("./code-uber/mapa.txt")
mapa1 = hacer_lectura('mapa_serializado.bin')
mapa1.draw_graph()
#dijkstra(mapa1,listv[0])
#printStatus(listv)
path = hacer_lectura('camino_serializado.bin')
print(path)

#printStatus(mapa1.vertices_list)
#dijkstra(mapa1,list(mapa1.vertices_list.values())[0])
#printStatus(mapa1.vertices_list)

#print(mapa_uber.adj_list[4])

#add_location(direcciones_mapa,'H1',[(e1,10),(e2,5)],None)
#add_location(direcciones_mapa,'C1',[(e1,8),(e2,5)],1200)
#add_location(direcciones_mapa,'P1',[(e3,10),(e5,5)],200)

#print(at_same_location(direcciones_mapa,'H1','C1'))
