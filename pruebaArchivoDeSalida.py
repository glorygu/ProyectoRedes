import sys

file_created = False

while file_created == False:
    output_file_name = raw_input("Ingrese el nombre de archivo de salida: ")
    try: 
        output_file = open (output_file_name, 'w+') 
    except IOError:
        print 'No se pudo abrir ', output_file_name
    else:
        
        print 'Se creo archivo de salida de manera exitosa. '
        file_created = True


for i in range (0, 9):
    output_file.write(raw_input(" "))

output_file.close()