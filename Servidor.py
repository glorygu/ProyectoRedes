# 
#   Universidad de Costa Rica
#
#   Desarrollado por: Gloriana Garro
#                     Jose Pablo Urena Gutierrez
#


import socket
import sys


print "-----------------------------------------------------"
print "    Bienvenido a Simulacion de Red 2016 - Servidor"
print "-----------------------------------------------------"
print "\n\n"
print "A continuacion ingrese los datos que se le solicitan"
print "\n\n"

# Variables de ingreso de datos

inter_port = input("Introduzca el puerto de escucha del servidor: ")

# Modo de trabajo

print "-----------------------------------------------------"
print "    Antes de iniciar, por favor indique el modo de ejecucion"
user_mode = input(" (1) Modo Normal (2) Modo Debug :  ")
print "\n\n"

if user_mode == 1:
    debug_mode = False
else:
    debug_mode = True


# -------------------- Creacion de archivo de salida ---------------------------

file_created = False

while file_created == False:
    output_file_name = raw_input("Ingrese el nombre de archivo de salida: ")
    try: 
        output_file = open (output_file_name, 'a') #w
    except IOError:
        print 'No se pudo abrir ', output_file_name
    else:
        if debug_mode:
            print 'Se creo archivo de salida de manera exitosa. '
        file_created = True
        
# ------------------------------------------------------------------------------        


caracteres = ""
ack_list = []
expected_sec_num = 1

# -------------------- Extraccion de paquetes ----------------------------------

def clear_list(input_list):
    size = len(input_list) 
    iterator = 1
    while iterator <= size:
        del input_list[size-iterator]
        iterator += 1


def extract_acks (initial_package):
    global expected_sec_num
    global caracteres
    iterator = 0
    size = len(initial_package)
    clear_list(ack_list)
    acks_in_order = True
    if debug_mode:
        print "           --------------------------------               "
        print "\n"
        print "\n Servidor esperando el (#) de secuencia siguiente: " + str (expected_sec_num)
    while (iterator < size and acks_in_order):
        #print initial_package[iterator]
        if initial_package[iterator] == '#':
            current_ack = ""
            iterator += 1
            while (iterator < size and initial_package[iterator] != '#' and initial_package[iterator] != ':'):
                #print initial_package[iterator]
                current_ack += initial_package[iterator]
                iterator += 1
            if debug_mode:
                print "Valor de secuencia en analisis: " + current_ack
            if int(current_ack) == expected_sec_num:
                ack_list.append(current_ack)
                expected_sec_num += 1
                
                if (initial_package[iterator] == ':'):
                    if (iterator+1 < len(initial_package)):
                        #output_file = open (output_file_name, 'w')
                        #print >>sys.stderr, 'valor de archivo: ', initial_package[iterator+1]
                        caracteres += initial_package[iterator+1]
                        open_file = open(output_file_name, "a")
                        open_file.write(initial_package[iterator+1])
                        open_file.close()
                        #output_file.close()
                
                # Ingresar valor a archivo de salida
                
            else:
                acks_in_order = False
        else:
            iterator+=1
    if debug_mode:
        print "\n"            
        print "           --------------------------------               \n"
    return ack_list

# ------------------------------------------------------------------------------



# --------------------- Socket para ingreso de trafico -------------------------

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', int(inter_port))
if debug_mode:
    print >>sys.stderr, 'Apertura de %s , en puerto de conexion: %s' % server_address
sock.bind(server_address)
sock.listen(1)

# ------------------------------------------------------------------------------

while True:
    
    connection, client_address = sock.accept()
 
    try:
        
        while True:
            data = connection.recv(1000)
            if debug_mode:
                print >>sys.stderr, 'Segmentos recibidos por puerto: "%s" \n' % data
            
            
            # Analizar lo recibido y reenviar acks al intermediario
            
            
            if data:
                
                # --------------------- Socket para envio de trafico -------------------------

                socket_intermediario = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_address = ('localhost', 10002)
                if debug_mode:
                    print >>sys.stderr, 'Inicio de conexion para envio de ACK hacia intermediario'
                socket_intermediario.connect(server_address)
                
                # ------------------------------------------------------------------------------
                
                try:
                    message = data
                    extract_acks(message)
                    iterator = 0 
                    for iterator in range(0, len(ack_list)):
                            socket_intermediario.sendall("#"+ack_list[iterator])
                            if debug_mode:
                                print "Enviando al cliente el ACK: " + ack_list[iterator]
                    
                finally:
                    socket_intermediario.close()
                
            else:
                if debug_mode:
                    print >>sys.stderr, 'El servidor no recibe mas datos por el momento.', client_address
                break
             
    finally:
        connection.close()