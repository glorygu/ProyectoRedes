import sys

def create_output_file():
    output_file_name = raw_input("Ingrese el nombre de archivo de salida: ")
    try: 
        file = open (output_file_name, 'w+') 
    except IOError:
        print 'No se pudo abrir ', output_file_name
    else:
        print 'Se creo archivo de salida de manera exitosa. '
        file.close()
    
    
create_output_file()