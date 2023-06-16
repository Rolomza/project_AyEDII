import sys
import os
from service import *

try:
    if(sys.argv[1] == "-create_map"):
        try:
            if (sys.argv[2] != ""):
                local_path = sys.argv[2]
                create_map(local_path)
        except:
            print("Local path not found. Insert -create_map <local_path>")
            

    if(os.path.isfile('map_serialized.bin')):

        if(sys.argv[1] == "-load_fix_element"): 
            try:
                if (sys.argv[2] != "" and sys.argv[3] != ""):
                    name_terminal_input = sys.argv[2]
                    address_terminal_input = sys.argv[3]
                    load_fix_element(name_terminal_input,address_terminal_input)
            except:
                print("Error. You must type: -load_fix_element <element_name> <address>")

        if(sys.argv[1] == "-load_movil_element"):
            try:
                if (sys.argv[2] != "" and sys.argv[3] != "" and sys.argv[4] != ""):
                    name_terminal_input = sys.argv[2]
                    address_terminal_input = sys.argv[3]
                    amount_terminal_input = int(sys.argv[4])
                    load_movil_element(name_terminal_input,address_terminal_input,amount_terminal_input)
                    map_elements = read_from_disk('map_elements_serialized.bin')
                    print(map_elements)
            except:
                print("Error. You must type: -load_movil_element <element_name> <address> <amount>")

        if(sys.argv[1] == "-create_trip"):
            try:
                if (sys.argv[2] != "" and sys.argv[3] != ""):
                    person_terminal_input = sys.argv[2]
                    address_or_element_terminal_input = sys.argv[3]
                    create_trip(person_terminal_input,address_or_element_terminal_input)
            except:
                print("Error. You must type: -create_trip <person> <address/element>")

    else:
        print("You must create a map first. Insert -create_map <local_path> to start.")

except IndexError:
    print("Insert -create_map <local_path> to start.")