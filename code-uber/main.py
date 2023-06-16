from uber import *
from dijkstra import *
from service import *



create_map("./code-uber/mapa.txt")
uber_map = read_from_disk('map_serialized.bin')
#mapa1.draw_graph()
path = read_from_disk('path_matrix_serialized.bin')
#print(path)
load_fix_element('H1',"<e8,20> <e10,30>")
load_movil_element('P1',"<e8,10> <e10,40>",2000)
load_movil_element('C1',"<e1,10> <e4,40>",200)
load_movil_element('C2',"<e1,60> <e2,40>",50)
load_movil_element('C3',"<e2,0> <e6,50>",110)
load_movil_element('C4',"<e9,35> <e10,15>",20)
load_movil_element('C5',"<e5,10> <e7,40>",25)
#map_elements = read_from_disk('map_elements_serialized.bin')
#print(map_elements)
#map_cars = {clave: valor for clave, valor in map_elements.items() if clave.startswith('C')}
#print(map_cars)
#print(map_cars['C1']['address'][0][0])
#print(uber_map.vertices_list[map_cars['C1']['address'][0][0]].key) #Esto me permitira buscar las filas de la matriz
#print(uber_map.draw_graph())
#uber_map.draw_graph()
create_trip(uber_map,'P1','H1')
#print(uber_map.vertices_list)
#print(uber_map.vertices_list)

#print(path[9])